import { FaGithub, FaLinkedin, FaEnvelope } from "react-icons/fa";

function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container footer-container">

        <div className="footer-left">
          <h2>CourseRec</h2>
          <p>
            Helping students discover the right courses based on
            their interests and skills.
          </p>
        </div>

        <div className="footer-center">
          <h4>Quick Links</h4>

          <a href="/">Home</a>
          <a href="/recommendations">Recommendations</a>
          <a href="/about">About</a>
        </div>

        <div className="footer-right">
          <h4>Connect</h4>

          <div className="social-icons">

            <a href="#">
              <FaGithub />
            </a>

            <a href="#">
              <FaLinkedin />
            </a>

            <a href="#">
              <FaEnvelope />
            </a>

          </div>
        </div>

      </div>

      <div className="copyright">
        © {year} CourseRec • Built with React & FastAPI
      </div>
    </footer>
  );
}

export default Footer;