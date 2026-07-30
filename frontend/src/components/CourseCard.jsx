import {
  FaArrowRight,
  FaBookOpen,
  FaClock,
  FaLayerGroup,
} from "react-icons/fa";

function CourseCard({ course }) {
  const {
    title = "Untitled Course",
    description = "No course description available.",
    domain = "General",
    difficulty = "Beginner",
    duration = null,
  } = course || {};

  const getDifficultyClass = () => {
    const level = String(difficulty).toLowerCase();

    if (level.includes("advanced")) {
      return "difficulty-advanced";
    }

    if (level.includes("intermediate")) {
      return "difficulty-intermediate";
    }

    return "difficulty-beginner";
  };

  return (
    <article className="course-card glass-card">
      <div className="course-card-top">
        <div className="course-category-icon">
          <FaBookOpen />
        </div>

        <span className={`difficulty-badge ${getDifficultyClass()}`}>
          {difficulty}
        </span>
      </div>

      <div className="course-card-content">
        <span className="course-provider">{domain}</span>

        <h3>{title}</h3>

        <p className="course-description">{description}</p>

        <div className="course-meta">
          <div className="course-meta-item">
            <FaLayerGroup />
            <span>{domain}</span>
          </div>

          <div className="course-meta-item">
            <FaClock />
            <span>
              {duration ? `${duration} hours` : "Self-paced"}
            </span>
          </div>
        </div>
      </div>

      <div className="course-card-footer">
        <button
          type="button"
          className="course-view-button"
          onClick={() =>
            alert("Enrollment feature coming soon!")
          }
        >
          Enroll
          <FaArrowRight />
        </button>
      </div>
    </article>
  );
}

export default CourseCard;