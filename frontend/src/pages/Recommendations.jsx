import StudentForm from "../components/StudentForm";
import {
  createStudent,
  getRecommendations,
} from "../services/api";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  FaBookOpen,
  FaExclamationTriangle,
  FaLightbulb,
} from "react-icons/fa";


import CourseCard from "../components/CourseCard";
import Loader from "../components/Loader";

function Recommendations() {
  const [courses, setCourses] = useState([]);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(false);
  }, []);

  const handleStudentSubmit = async (student) => {
    setSearching(true);
    setError("");

    try {
      const createdStudent = await createStudent(student);

      const data = await getRecommendations(
        createdStudent.student_id
      );

      setRecommendation(data);
      setCourses(data.courses);
    } catch (err) {
      setError(err.message);
    } finally {
      setSearching(false);
    }
  };

  if (loading) {
    return (
      <div className="page recommendations-page">
        <Loader message="Loading available courses from the database..." />
      </div>
    );
  }

  return (
    <div className="page recommendations-page">
      <motion.section
        className="recommendations-header"
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.55 }}
      >
        <div className="recommendations-header-icon">
          <FaLightbulb />
        </div>

        <div>
          <span className="recommendations-eyebrow">
            Personalized discovery
          </span>

          <h1>Find courses that match your goals</h1>

          <p>
            Search by your interests and apply filters to discover courses
            suited to your preferred learning level and schedule.
          </p>
        </div>
      </motion.section>

      {error && (
        <div className="backend-warning">
          <FaExclamationTriangle />

          <div>
            <strong>Backend connection notice</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      <StudentForm
          onSubmit={handleStudentSubmit}
          loading={searching}
      />

      {searching ? (
        <Loader message="Comparing your preferences with available courses..." />
      ) : (
        <section className="recommendation-results">
          <div className="results-heading">
            <div>
              <span className="results-label">
                <FaBookOpen />
                Course results
              </span>

              <h2>
                {recommendation
                    ? `Recommended Learning Path`
                    : "Generate Your Learning Path"}
            </h2>

              <p>
                {courses.length}{" "}
                {courses.length === 1 ? "course" : "courses"} found
              </p>
            </div>
          </div>

            {recommendation && (
              <motion.div
                className="glass-card recommendation-summary"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
              >
                <div className="summary-header">
                  <div>
                    <span className="recommendations-eyebrow">
                      AI Recommendation
                    </span>

                    <h3>Your Personalized Learning Path</h3>

                  </div>
                </div>

                <div className="summary-stats">

                  <div className="summary-stat glass-card">
                    <span className="summary-label">
                      Predicted Domain
                    </span>

                    <h2>{recommendation.predicted_domain}</h2>
                  </div>

                  <div className="summary-stat glass-card">
                    <span className="summary-label">
                      Recommended Level
                    </span>

                    <h2>{recommendation.recommended_difficulty}</h2>
                  </div>

                  <div className="summary-stat glass-card">
                    <span className="summary-label">
                      AI Confidence
                    </span>

                    <h2>
                      {(recommendation.confidence * 100).toFixed(1)}%
                    </h2>
                  </div>

                  <div className="summary-stat glass-card">
                    <span className="summary-label">
                      Courses Suggested
                    </span>

                    <h2>{courses.length}</h2>
                  </div>

                </div>

          
              </motion.div>
            )}
          {courses.length > 0 ? (
            <div className="course-results-grid">
              {courses.map((course, index) => (
                <motion.div
                  key={course.id}
                  initial={{ opacity: 0, y: 28 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    duration: 0.42,
                    delay: index * 0.07,
                  }}
                >
                  <CourseCard course={course} />
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="no-results-card glass-card">
              <div className="no-results-icon">
                <FaBookOpen />
              </div>

              <h3>No matching courses found</h3>

              <p>
                Try using a broader interest, changing the difficulty level, or
                selecting a longer duration.
              </p>

              <button
                type="button"
                className="primary-btn"
                onClick={() => {
                    setRecommendation(null);
                    setCourses([]);
                }}
            >
                Clear Results
            </button>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

export default Recommendations;