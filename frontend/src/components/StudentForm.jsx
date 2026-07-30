import { useState } from "react";
import { FaGraduationCap } from "react-icons/fa";

function StudentForm({ onSubmit, loading }) {
  const [student, setStudent] = useState({
    name: "",
    email: "",
    degree: "",
    branch: "",
    semester: 1,
    cgpa: "",
    interests: "",
    learning_style: "",
    career_goal: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setStudent((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const submit = (e) => {
    e.preventDefault();

    onSubmit({
      ...student,
      semester: Number(student.semester),
      cgpa: Number(student.cgpa),
    });
  };

  return (
    <div className="course-search-card glass-card">
      <div className="search-card-heading">
        <div className="search-heading-icon">
          <FaGraduationCap />
        </div>

        <div>
          <span className="search-eyebrow">
            AI Recommendation
          </span>

          <h2>Tell us about yourself</h2>

          <p>
            Fill in your profile to receive personalized course recommendations.
          </p>
        </div>
      </div>

      <form className="course-search-form" onSubmit={submit}>
        <input
        name="name"
        placeholder="Full Name"
        value={student.name}
        onChange={handleChange}
        required
        />

        <input
        name="email"
        type="email"
        placeholder="Email Address"
        value={student.email}
        onChange={handleChange}
        required
        />

        <input
        name="degree"
        placeholder="Degree (e.g. B.Tech, B.Sc, BCA)"
        value={student.degree}
        onChange={handleChange}
        required
        />

        <input
        name="branch"
        placeholder="Branch (e.g. CSE, AI, IT, ECE)"
        value={student.branch}
        onChange={handleChange}
        required
        />

        <input
        type="number"
        min="1"
        max="8"
        name="semester"
        placeholder="Current Semester"
        value={student.semester}
        onChange={handleChange}
        required
        />

        <input
        type="number"
        step="0.1"
        min="0"
        max="10"
        name="cgpa"
        placeholder="Current CGPA (e.g. 8.5)"
        value={student.cgpa}
        onChange={handleChange}
        required
        />

        <input
        name="interests"
        placeholder="Interests (e.g. Python, AI, Web Development)"
        value={student.interests}
        onChange={handleChange}
        required
        />

        <input
        name="learning_style"
        placeholder="Learning Style (Video, Reading, Hands-on)"
        value={student.learning_style}
        onChange={handleChange}
        required
        />

        <input
        name="career_goal"
        placeholder="Career Goal (e.g. ML Engineer, Cloud Engineer)"
        value={student.career_goal}
        onChange={handleChange}
        required
        />

        <button
          className="primary-btn"
          disabled={loading}
        >
          {loading
            ? "Generating..."
            : "Generate Recommendations"}
        </button>

      </form>
    </div>
  );
}

export default StudentForm;