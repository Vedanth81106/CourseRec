import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { FaGraduationCap, FaBars, FaTimes } from "react-icons/fa";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const closeMenu = () => {
    setMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="container navbar-container">

        <Link to="/" className="logo" onClick={closeMenu}>
          <FaGraduationCap className="logo-icon" />
          <span>CourseRec</span>
        </Link>

        <ul className={menuOpen ? "nav-links active" : "nav-links"}>
          <li>
            <Link
              to="/"
              className={location.pathname === "/" ? "active-link" : ""}
              onClick={closeMenu}
            >
              Home
            </Link>
          </li>

          <li>
            <Link
              to="/recommendations"
              className={
                location.pathname === "/recommendations"
                  ? "active-link"
                  : ""
              }
              onClick={closeMenu}
            >
              Recommendations
            </Link>
          </li>

          <li>
            <Link
              to="/about"
              className={location.pathname === "/about" ? "active-link" : ""}
              onClick={closeMenu}
            >
              About
            </Link>
          </li>
        </ul>

        <button
          className="menu-btn"
          onClick={toggleMenu}
        >
          {menuOpen ? <FaTimes /> : <FaBars />}
        </button>

      </div>
    </nav>
  );
}

export default Navbar;