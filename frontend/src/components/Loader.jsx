import { FaBookOpen } from "react-icons/fa";

function Loader({ message = "Finding the best courses for you..." }) {
  return (
    <div className="loader-container">
      <div className="loader-animation">
        <div className="loader-ring"></div>

        <div className="loader-icon">
          <FaBookOpen />
        </div>
      </div>

      <h3>Searching courses</h3>
      <p>{message}</p>

      <div className="loader-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
}

export default Loader;