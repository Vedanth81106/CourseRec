import SearchBar from "../components/SearchBar";
import { getCourses } from "../services/api";
import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  FaBookOpen,
  FaExclamationTriangle,
  FaFilter,
  FaLightbulb,
} from "react-icons/fa";


import CourseCard from "../components/CourseCard";
import Loader from "../components/Loader";

function Recommendations() {
  const [courses, setCourses] = useState([]);
  const [searchData, setSearchData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState("");

  const sampleCourses = [
    {
      id: 1,
      title: "Python for Beginners",
      description:
        "Learn Python fundamentals including variables, loops, functions, lists, and object-oriented programming.",
      category: "Programming",
      difficulty: "Beginner",
      duration: 8,
      rating: 4.8,
      provider: "CourseRec",
    },
    {
      id: 2,
      title: "Modern Web Development",
      description:
        "Build responsive websites using HTML, CSS, JavaScript, React, and modern frontend development techniques.",
      category: "Web Development",
      difficulty: "Beginner",
      duration: 12,
      rating: 4.7,
      provider: "CourseRec",
    },
    {
      id: 3,
      title: "Machine Learning Fundamentals",
      description:
        "Understand supervised learning, classification, regression, model evaluation, and common machine learning algorithms.",
      category: "Machine Learning",
      difficulty: "Intermediate",
      duration: 12,
      rating: 4.9,
      provider: "CourseRec",
    },
    {
      id: 4,
      title: "UI/UX Design Essentials",
      description:
        "Learn user research, wireframing, prototyping, visual hierarchy, and usability principles for digital products.",
      category: "UI/UX",
      difficulty: "Beginner",
      duration: 6,
      rating: 4.6,
      provider: "CourseRec",
    },
    {
      id: 5,
      title: "Advanced Java Programming",
      description:
        "Explore collections, multithreading, exception handling, JDBC, design patterns, and advanced Java concepts.",
      category: "Programming",
      difficulty: "Advanced",
      duration: 16,
      rating: 4.5,
      provider: "CourseRec",
    },
    {
      id: 6,
      title: "Data Science with Python",
      description:
        "Use Python, NumPy, Pandas, and data visualization tools to clean, analyze, and understand datasets.",
      category: "Data Science",
      difficulty: "Intermediate",
      duration: 10,
      rating: 4.8,
      provider: "CourseRec",
    },
  ];

  useEffect(() => {
    fetchCourses();
  }, []);

  const normalizeCourse = (course, index) => {
    return {
      id: course.id ?? course.course_id ?? index + 1,

      title:
        course.title ??
        course.course_name ??
        course.name ??
        "Untitled Course",

      description:
        course.description ??
        course.course_description ??
        course.summary ??
        "No description is available for this course.",

      category:
        course.category ??
        course.domain ??
        course.subject ??
        course.skills ??
        "General",

      difficulty:
        course.difficulty ??
        course.level ??
        course.course_level ??
        "Beginner",

      duration:
        course.duration ??
        course.duration_weeks ??
        course.course_duration ??
        "Flexible",

      rating: Number(course.rating ?? course.score ?? 4.5),

      provider:
        course.provider ??
        course.platform ??
        course.institution ??
        "CourseRec",
    };
  };

  const fetchCourses = async () => {
    setLoading(true);
    setError("");

    try {

      const data = await getCourses();

      const courseList = Array.isArray(data)
        ? data
        : data.courses || data.results || [];

      const normalizedCourses = courseList.map(normalizeCourse);

      setCourses(
        normalizedCourses.length > 0 ? normalizedCourses : sampleCourses
      );
    } catch (fetchError) {
      console.error("Course loading error:", fetchError);

      setCourses(sampleCourses);

      setError(
        "The backend could not be reached, so sample courses are being displayed."
      );
    } finally {
      setLoading(false);
    }
  };

  const filteredCourses = useMemo(() => {
    if (!searchData) {
      return courses;
    }

    const searchTerm = searchData.interest.toLowerCase();

    return courses.filter((course) => {
      const searchableText = [
        course.title,
        course.description,
        course.category,
        course.provider,
      ]
        .join(" ")
        .toLowerCase();

      const matchesInterest = searchableText.includes(searchTerm);

      const matchesDifficulty =
        !searchData.difficulty ||
        String(course.difficulty).toLowerCase() ===
          searchData.difficulty.toLowerCase();

      const numericDuration = Number(course.duration);

      const matchesDuration =
        !searchData.maxDuration ||
        Number.isNaN(numericDuration) ||
        numericDuration <= searchData.maxDuration;

      return matchesInterest && matchesDifficulty && matchesDuration;
    });
  }, [courses, searchData]);

  const handleSearch = (formData) => {
    if (!formData) {
      setSearchData(null);
      return;
    }

    setSearching(true);
    setSearchData(formData);

    window.setTimeout(() => {
      setSearching(false);
    }, 700);
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

      <SearchBar onSearch={handleSearch} loading={searching} />

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
                {searchData
                  ? `Recommended for “${searchData.interest}”`
                  : "Explore available courses"}
              </h2>

              <p>
                {filteredCourses.length}{" "}
                {filteredCourses.length === 1 ? "course" : "courses"} found
              </p>
            </div>

            {searchData && (
              <div className="active-filter-summary">
                <FaFilter />

                <div>
                  <span>Active filters</span>

                  <strong>
                    {searchData.difficulty || "Any level"}
                    {" · "}
                    {searchData.maxDuration
                      ? `Up to ${searchData.maxDuration} weeks`
                      : "Any duration"}
                  </strong>
                </div>
              </div>
            )}
          </div>

          {filteredCourses.length > 0 ? (
            <div className="course-results-grid">
              {filteredCourses.map((course, index) => (
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
                onClick={() => setSearchData(null)}
              >
                Show All Courses
              </button>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

export default Recommendations;