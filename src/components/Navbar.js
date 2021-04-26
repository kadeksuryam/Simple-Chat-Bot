import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { FaBars, FaTimes } from 'react-icons/fa'
import './navbar.css'

const Navbar = () => {
    const [click, setClick] = useState(false)
    const [mobileSize, setmobileSize] = useState(false);

    const handleClick = () => setClick(!click && mobileSize)

    const handleResize = () => {
       //console.log(window.innerWidth)
       if(window.innerWidth <= 960) setmobileSize(true);
       else setmobileSize(false); 
    }

    window.addEventListener('resize', handleResize);

    return(
        <>
            <div className="navbar">
                <div className="navbar-container container">
                    <Link to="/" className="navbar-logo">
                        Hayacaka
                    </Link>
                    <div className="menu-icon" onClick={handleClick}>
                        {click ? <FaTimes/> : <FaBars/>}
                    </div>
                    <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                        <li className="nav-item">
                            <Link to='/' onClick={handleClick} className="nav-links">
                                Home
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to='/about' onClick={handleClick} className="nav-links">
                                About Us
                            </Link>
                        </li>
                    </ul>
                </div>
            </div>
        </>
    )
}

export default Navbar