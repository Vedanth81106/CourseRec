import { useState } from "react";
import {
  FaBookOpen,
  FaClock,
  FaGraduationCap,
  FaSearch,
} from "react-icons/fa";

function SearchBar({ onSearch, loading = false }) {
  const [formData, setFormData] = useState({
    interest: "",
    difficulty: "",
    maxDuration: "",
  });

  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));

    if (error) {
      setError("");
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!formData.interest.trim()) {
      setError("Please enter an interest or course field.");
      return;
    }

    setError("");

    if (onSearch) {
      onSearch({
        interest: formData.interest.trim(),
        difficulty: formData.difficulty,
        maxDuration: formData.maxDuration
          ? Number(formData.maxDuration)
          : null,
      });
    }
  };

  const handleReset = () => {
    const emptyForm = {
      interest: "",
      difficulty: "",
      maxDuration: "",
    };

    setFormData(emptyForm);
    setError("");

    if (onSearch) {
      onSearch(null);
    }
  };

  return (
    <div className="course-search-card glass-card">
      <div className="search-card-heading">
        <div className="search-heading-icon">
          <FaGraduationCap />
        </div>

        <div>
          <span className="search-eyebrow">Personalized search</span>
          <h2>What would you like to learn?</h2>
          <p>
            Enter your preferred field and choose optional filters to find
            suitable courses.
          </p>
        </div>
      </div>

      <form className="course-search-form" onSubmit={handleSubmit}>
        <div className="search-field search-field-large">
          <label htmlFor="interest">
            <FaBookOpen />
            Interest or domain
          </label>

          <div className="input-wrapper">
            <FaSearch className="input-icon" />

            <input
              id="interest"
              name="interest"
              type="text"
              value={formData.interest}
              onChange={handleChange}
              placeholder="Example: Python, web development, AI..."
              autoComplete="off"
            />
          </div>
        </div>

        <div className="search-field">
          <label htmlFor="difficulty">
            <FaGraduationCap />
            Difficulty
          </label>

          <select
            id="difficulty"
            name="difficulty"
            value={formData.difficulty}
            onChange={handleChange}
          >
            <option value="">Any level</option>
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
        </div>

        <div className="search-field">
          <label htmlFor="maxDuration">
            <FaClock />
            Maximum duration
          </label>

          <select
            id="maxDuration"
            name="maxDuration"
            value={formData.maxDuration}
            onChange={handleChange}
          >
            <option value="">Any duration</option>
            <option value="4">Up to 4 weeks</option>
            <option value="8">Up to 8 weeks</option>
            <option value="12">Up to 12 weeks</option>
            <option value="24">Up to 24 weeks</option>
          </select>
        </div>

        <div className="search-form-actions">
          <button
            type="submit"
            className="primary-btn search-submit-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="button-spinner"></span>
                Finding courses...
              </>
            ) : (
              <>
                <FaSearch />
                Find Courses
              </>
            )}
          </button>

          <button
            type="button"
            className="search-reset-btn"
            onClick={handleReset}
            disabled={loading}
          >
            Clear
          </button>
        </div>
      </form>

      {error && <p className="search-error">{error}</p>}

      <div className="search-suggestions">
        <span>Popular searches:</span>

        {["Python", "Web Development", "Machine Learning", "UI/UX"].map(
          (suggestion) => (
            <button
              type="button"
              key={suggestion}
              onClick={() =>
                setFormData((previousData) => ({
                  ...previousData,
                  interest: suggestion,
                }))
              }
            >
              {suggestion}
            </button>
          )
        )}
      </div>
    </div>
  );
}

export default SearchBar;