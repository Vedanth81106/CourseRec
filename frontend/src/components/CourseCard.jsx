import {
  FaArrowRight,
  FaBookOpen,
  FaClock,
  FaLayerGroup,
  FaStar,
} from "react-icons/fa";

function CourseCard({ course }) {
  const {
    title = "Untitled Course",
    description = "No course description is available.",
    category = "General",
    difficulty = "Beginner",
    duration = "Flexible",
    rating = 4.5,
    provider = "CourseRec",
  } = course || {};

  const getDifficultyClass = () => {
    const normalizedDifficulty = String(difficulty).toLowerCase();

    if (normalizedDifficulty.includes("advanced")) {
      return "difficulty-advanced";
    }

    if (normalizedDifficulty.includes("intermediate")) {
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
        <span className="course-provider">{provider}</span>

        <h3>{title}</h3>

        <p className="course-description">{description}</p>

        <div className="course-meta">
          <div className="course-meta-item">
            <FaLayerGroup />
            <span>{category}</span>
          </div>

          <div className="course-meta-item">
            <FaClock />
            <span>
              {typeof duration === "number"
                ? `${duration} weeks`
                : duration}
            </span>
          </div>
        </div>
      </div>

      <div className="course-card-footer">
        <div className="course-rating">
          <FaStar />
          <strong>{rating}</strong>
          <span>/ 5</span>
        </div>

        <button type="button" className="course-view-button">
          View Course
          <FaArrowRight />
        </button>
      </div>
    </article>
  );
}

export default CourseCard;