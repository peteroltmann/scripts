//!
//! \file ClassName.hpp
//! \author First Last (shrt)
//! \date dd.mm.yyyy
//!
//! \brief <Description>
//!

#ifndef PACKAGENAME_CLASSNAME_HPP_SEEN
#define PACKAGENAME_CLASSNAME_HPP_SEEN

namespace packagename {

//! \brief Brief description of class responsibilities and role
//!
//! Detailed design and verbose description, dependencies, lifecycle, states, ...
class ClassName
{
public:
    //! \brief Default constructor.
    ClassName() = default;
 
    //! \brief Default copy constructor.
    ClassName(const ClassName&) = default;
 
    //! \brief Default move constructor.
    ClassName(ClassName&&) = default;
 
    //! \brief Default destructor.
    ~ClassName() = default;
 
    //!
    //! \brief Default assignment operator.
    //! \return Reference to this
    //!
    ClassName& operator=(const ClassName&) = default;
 
    //!
    //! \brief Default move-assignment operator.
    //! \return Reference to this
    //!
    ClassName& operator=(ClassName&&) = default;

private:
    $0
 
}; // ClassName

} // namespace packagename

#endif // PACKAGENAME_CLASSNAME_HPP_SEEN
