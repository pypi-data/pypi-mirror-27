
#include "DB_Elements.hpp"
#include "DB_Nodes.hpp"
#include "DB_Parts.hpp"
#include "Element.hpp"
#include "FEMFile.hpp"
#include "Node.hpp"
#include "Part.hpp"

namespace qd {

/** Constructor
 *
 * @param FEMFile* _femfile : parent file
 */
DB_Elements::DB_Elements(FEMFile* _femfile)
  : femfile(_femfile)
  , db_nodes(_femfile->get_db_nodes())
  , db_parts(_femfile->get_db_parts())
{
}

/*
 * Destructor.
 */
DB_Elements::~DB_Elements()
{
#ifdef QD_DEBUG
  std::cout << "DB_Elements::~DB_Elements called." << std::endl;
#endif
}

/** Add an element coming from a D3plot file
 *
 * @param ElementType _eType : type of the element to add, enum in Element.hpp
 * @param int32_t _elementID : id of the element to add
 * @param std::vector<int32_t> _elementData : element data from d3plot, node
 * ids and
 * part
 * id
 * @return std::shared_ptr<Element> element : pointer to created instance
 *
 * Add an element to the db by it's ID  and it's nodeIndexes. Throws an
 * exception
 * if one nodeIndex is invalid or if the elementID is already existing.
 */
std::shared_ptr<Element>
DB_Elements::add_element_byD3plot(const Element::ElementType _eType,
                                  const int32_t _elementID,
                                  const std::vector<int32_t>& _elementData)
{
  if (_elementID < 0) {
    throw(std::invalid_argument("Element-ID may not be negative!"));
  }

  // Find part
  // index is decremented once, since ls-dyna starts at 1 (fortran array style)
  const auto part = this->db_parts->get_partByIndex(_elementData.back() - 1);
  if (part == nullptr) {
    throw(std::invalid_argument(
      "Could not find part with index:" + std::to_string(_elementData.back()) +
      " in db."));
  }

  // Find nodes
  std::set<int32_t> node_ids; // just for testing
  std::vector<std::shared_ptr<Node>> nodes;
  std::vector<size_t> node_indexes;
  for (size_t iNode = 0; iNode < _elementData.size() - 1;
       iNode++) { // last is mat

    // dyna starts at index 1 (fortran), this program at 0 of course
    auto _node = this->db_nodes->get_nodeByIndex(_elementData[iNode] - 1);

    // check if duplicate
    auto tmp = node_ids.size();
    node_ids.insert(_elementData[iNode]);
    if (node_ids.size() == tmp)
      continue;

    // add new node data
    nodes.push_back(_node);
    node_indexes.push_back(_elementData[iNode] - 1);
  }

  // Create element
  std::shared_ptr<Element> element =
    std::make_shared<Element>(_elementID, _eType, node_indexes, this);

  if (_eType == Element::BEAM) {
    auto it = this->id2index_elements2.find(_elementID);
    if (it != this->id2index_elements2.end()) {
      throw(std::invalid_argument(
        "Trying to insert an element with same id twice:" +
        std::to_string(_elementID)));
    }

    this->id2index_elements2.insert(
      std::pair<int32_t, size_t>(_elementID, this->elements2.size()));
    this->elements2.push_back(element);

  } else if (_eType == Element::SHELL) {
    auto it = this->id2index_elements4.find(_elementID);
    if (it != this->id2index_elements4.end()) {
      throw(std::invalid_argument(
        "Trying to insert an element with same id twice:" +
        std::to_string(_elementID)));
    }

    this->id2index_elements4.insert(
      std::pair<int32_t, size_t>(_elementID, this->elements4.size()));
    this->elements4.push_back(element);

  } else if (_eType == Element::SOLID) {
    auto it = this->id2index_elements8.find(_elementID);
    if (it != this->id2index_elements8.end()) {
      throw(std::invalid_argument(
        "Trying to insert an element with same id twice:" +
        std::to_string(_elementID)));
    }

    this->id2index_elements8.insert(
      std::pair<int32_t, size_t>(_elementID, this->elements8.size()));
    this->elements8.push_back(element);

  } else if (_eType == Element::TSHELL) {
    auto it = this->id2index_elements4th.find(_elementID);
    if (it != this->id2index_elements4th.end()) {
      throw(std::invalid_argument(
        "Trying to insert an element with same id twice:" +
        std::to_string(_elementID)));
    }

    this->id2index_elements4th.insert(
      std::pair<int32_t, size_t>(_elementID, this->elements4th.size()));
    this->elements4th.push_back(element);

  } else {
    throw(std::invalid_argument(
      "Element with unknown element type was tried to get inserted "
      "into the database."));
  }

  // Register Elements
  for (auto& node : nodes) {
    node->add_element(element);
  }
  part->add_element(element);

  return element;
}

/** Add an element coming from a KeyFile/Dyna Input File
 *
 * @param Element::ElementType _eType : type of the element to add, enum in
 * Element.hpp
 * @param int32_t _elementID : id of the element to add
 * @param int32_t part_id : id of the part, the element belongs to
 * @param std::vector<int32_t> _node_ids : node ids of the used nodes
 * @return std::shared_ptr<Element> element : pointer to created instance
 *
 * Add an element to the db by it's ID  and it's nodeIDs. Throws an exception
 * if one nodeID is invalid or if the elementID is already existing. Since a
 * KeyFile may have some weird order, missing parts and nodes are created.
 */
std::shared_ptr<Element>
DB_Elements::add_element_byKeyFile(Element::ElementType _eType,
                                   int32_t _elementID,
                                   int32_t _partid,
                                   std::vector<int32_t> _node_ids)
{
  if (_elementID < 0) {
    throw(std::invalid_argument("Element-ID may not be negative!"));
  }

  // Find part (inefficient)
  std::shared_ptr<Part> part = nullptr;
  try {
    part = this->db_parts->get_partByID(_partid);
  } catch (std::invalid_argument) {
    part = this->db_parts->add_partByID(_partid);
  }

  // Find nodes
  std::set<int32_t> node_ids;
  std::vector<std::shared_ptr<Node>> nodes;
  std::vector<size_t> node_indexes;
  for (size_t iNode = 0; iNode < _node_ids.size(); ++iNode) {

    auto _node = this->db_nodes->get_nodeByID(_node_ids[iNode]);

    // check node existance
    if (_node == nullptr)
      _node =
        this->db_nodes->add_node(_node_ids[iNode], std::vector<float>(3, 0.0f));

    // check if duplicate
    auto tmp = node_ids.size();
    node_ids.insert(_node_ids[iNode]);
    if (node_ids.size() == tmp)
      continue;

    // save node data
    nodes.push_back(_node);
    node_indexes.push_back(this->db_nodes->get_index_from_id(_node_ids[iNode]));
  }

  // Create element
  std::shared_ptr<Element> element =
    std::make_shared<Element>(_elementID, _eType, node_indexes, this);

  if (_eType == Element::BEAM) {
    auto it = this->id2index_elements2.find(_elementID);
    if (it != this->id2index_elements2.end()) {
      throw(std::invalid_argument(
        "Trying to insert an element with same id twice:" +
        std::to_string(_elementID)));
    }

    this->id2index_elements2.insert(
      std::pair<int32_t, size_t>(_elementID, this->elements2.size()));
    this->elements2.push_back(element);

  } else if (_eType == Element::SHELL) {
    auto it = this->id2index_elements4.find(_elementID);
    if (it != this->id2index_elements4.end()) {
      throw(std::invalid_argument(
        "Trying to insert an element with same id twice:" +
        std::to_string(_elementID)));
    }

    this->id2index_elements4.insert(
      std::pair<int32_t, size_t>(_elementID, this->elements4.size()));
    this->elements4.push_back(element);

  } else if (_eType == Element::SOLID) {
    auto it = this->id2index_elements8.find(_elementID);
    if (it != this->id2index_elements8.end()) {
      throw(std::invalid_argument(
        "Trying to insert an element with same id twice:" +
        std::to_string(_elementID)));
    }

    this->id2index_elements8.insert(
      std::pair<int32_t, size_t>(_elementID, this->elements8.size()));
    this->elements8.push_back(element);

  } else if (_eType == Element::TSHELL) {
    auto it = this->id2index_elements4th.find(_elementID);
    if (it != this->id2index_elements4th.end()) {
      throw(std::invalid_argument(
        "Trying to insert an element with same id twice:" +
        std::to_string(_elementID)));
    }

    this->id2index_elements4th.insert(
      std::pair<int32_t, size_t>(_elementID, this->elements4th.size()));
    this->elements4th.push_back(element);

  } else {
    throw(std::invalid_argument(
      "Element with unknown element type was tried to get inserted "
      "into the database."));
  }

  // Register Elements
  for (auto& node : nodes) {
    node->add_element(element);
  }
  part->add_element(element);

  return std::move(element);
}

/** Get the DynaInputFile pointer
 * @return DnyaInputFile* keyfile
 */
FEMFile*
DB_Elements::get_femfile()
{
  return this->femfile;
}

/** Get the node-db.
 * @return DB_Nodes* db_nodes
 */
DB_Nodes*
DB_Elements::get_db_nodes()
{
  return this->db_nodes;
}

/** Reserve memory for future elements
 * @param _type element type to apply reserve on
 * @param _size size to reserve internally
 *
 * Does nothing if _type is NONE.
 */
void
DB_Elements::reserve(const Element::ElementType _type, const size_t _size)
{
  if (_type == Element::BEAM) {
    elements2.reserve(_size);
  } else if (_type == Element::SHELL) {
    elements4.reserve(_size);
  } else if (_type == Element::SOLID) {
    elements8.reserve(_size);
  } else if (_type == Element::TSHELL) {
    elements4th.reserve(_size);
  } else {
    throw std::invalid_argument(
      "Can not reverse memory for an unknown ElementType: " +
      std::to_string(_type));
  }
}

/** Get the number of  in the db.
 * @return unsigned int32_t nElements : returns the total number of elements in
 * the
 * db
 */
size_t
DB_Elements::get_nElements(const Element::ElementType _type) const
{
  if (_type == Element::BEAM) {
    return elements2.size();
  } else if (_type == Element::SHELL) {
    return elements4.size();
  } else if (_type == Element::SOLID) {
    return elements8.size();
  } else if (_type == Element::TSHELL) {
    return elements4th.size();
  }
  return elements4.size() + elements2.size() + elements8.size() +
         elements4th.size();
}

/** Get the elements of the database of a certain type
 *
 * @param _type : optional filtering type
 * @return elems : std::vector of elements
 */
std::vector<std::shared_ptr<Element>>
DB_Elements::get_elements(const Element::ElementType _type)
{

  if (_type == Element::NONE) {
    std::vector<std::shared_ptr<Element>> elems;
    elems.reserve(this->get_nElements(_type));
    elems.insert(elems.end(), elements2.begin(), elements2.end());
    elems.insert(elems.end(), elements4.begin(), elements4.end());
    elems.insert(elems.end(), elements8.begin(), elements8.end());
    elems.insert(elems.end(), elements4th.begin(), elements4th.end());
    return elems;

  } else if (_type == Element::BEAM) {
    return elements2;

  } else if (_type == Element::SHELL) {
    return elements4;

  } else if (_type == Element::SOLID) {
    return elements8;

  } else if (_type == Element::TSHELL) {
    return elements4th;
  }

  throw(std::invalid_argument("Unknown element type specified."));
}

} // namespace qd