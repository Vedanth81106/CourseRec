import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
  FaArrowRight,
  FaBookOpen,
  FaBrain,
  FaChartLine,
  FaCheckCircle,
  FaCode,
  FaLaptopCode,
  FaPalette,
} from "react-icons/fa";

function Home() {
  const features = [
    {
      icon: <FaBrain />,
      title: "Smart Suggestions",
      description:
        "Receive course recommendations based on your interests, skills, and learning goals.",
    },
    {
      icon: <FaBookOpen />,
      title: "Explore Courses",
      description:
        "Discover useful courses from different domains and find what suits you best.",
    },
    {
      icon: <FaChartLine />,
      title: "Improve Your Skills",
      description:
        "Choose courses that help you strengthen your knowledge and career opportunities.",
    },
  ];

  const categories = [
    {
      icon: <FaLaptopCode />,
      title: "Web Development",
      courseCount: "Frontend and backend",
    },
    {
      icon: <FaCode />,
      title: "Programming",
      courseCount: "Python, Java and more",
    },
    {
      icon: <FaBrain />,
      title: "Artificial Intelligence",
      courseCount: "AI and machine learning",
    },
    {
      icon: <FaPalette />,
      title: "UI/UX Design",
      courseCount: "Design and creativity",
    },
  ];

  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-decoration hero-decoration-one"></div>
        <div className="hero-decoration hero-decoration-two"></div>

        <div className="container hero-container">
          <motion.div
            className="hero-content"
            initial={{ opacity: 0, x: -45 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
          >
            <div className="hero-badge">
              <FaCheckCircle />
              Personalized learning made simple
            </div>

            <h1>
              Find the perfect course for your
              <span> learning journey.</span>
            </h1>

            <p>
              Tell us what you are interested in and CourseRec will help you
              discover courses that match your skills, preferences, and goals.
            </p>

            <div className="hero-actions">
              <Link to="/recommendations" className="primary-btn hero-button">
                Get Recommendations
                <FaArrowRight />
              </Link>

              <Link to="/about" className="secondary-btn">
                Learn More
              </Link>
            </div>

            <div className="hero-highlights">
              <div>
                <strong>Smart</strong>
                <span>Recommendations</span>
              </div>

              <div>
                <strong>Simple</strong>
                <span>User Experience</span>
              </div>

              <div>
                <strong>Useful</strong>
                <span>Learning Paths</span>
              </div>
            </div>
          </motion.div>

          <motion.div
            className="hero-visual"
            initial={{ opacity: 0, scale: 0.85 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.15 }}
          >
            <div className="recommendation-preview glass-card">
              <div className="preview-header">
                <div>
                  <span className="preview-label">Your recommendation</span>
                  <h3>Courses selected for you</h3>
                </div>

                <div className="preview-icon">
                  <FaBrain />
                </div>
              </div>

              <div className="preview-course">
                <div className="course-number">01</div>

                <div>
                  <h4>Python for Beginners</h4>
                  <p>Programming • Beginner</p>
                </div>

                <span className="match-score">96% match</span>
              </div>

              <div className="preview-course">
                <div className="course-number">02</div>

                <div>
                  <h4>Machine Learning Basics</h4>
                  <p>Artificial Intelligence • Intermediate</p>
                </div>

                <span className="match-score">91% match</span>
              </div>

              <div className="preview-course">
                <div className="course-number">03</div>

                <div>
                  <h4>Modern Web Development</h4>
                  <p>Development • Beginner</p>
                </div>

                <span className="match-score">87% match</span>
              </div>

              <div className="preview-footer">
                <span>Recommendations ready</span>
                <FaCheckCircle />
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="section page">
        <div className="section-heading">
          <span className="section-tag">Why CourseRec?</span>
          <h2 className="section-title">
            A smarter way to choose what to learn
          </h2>
          <p className="section-subtitle">
            Instead of searching through hundreds of courses, get suggestions
            designed around your interests and goals.
          </p>
        </div>

        <div className="grid grid-3 features-grid">
          {features.map((feature, index) => (
            <motion.article
              className="feature-card glass-card"
              key={feature.title}
              initial={{ opacity: 0, y: 35 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.25 }}
              transition={{ duration: 0.5, delay: index * 0.12 }}
            >
              <div className="feature-icon">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </motion.article>
          ))}
        </div>
      </section>

      <section className="section categories-section">
        <div className="page">
          <div className="section-heading">
            <span className="section-tag">Popular fields</span>
            <h2 className="section-title">Explore different learning areas</h2>
            <p className="section-subtitle">
              Browse popular categories and identify the field that matches
              your interests.
            </p>
          </div>

          <div className="category-grid">
            {categories.map((category, index) => (
              <motion.div
                className="category-card"
                key={category.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.45, delay: index * 0.1 }}
                whileHover={{ y: -8 }}
              >
                <div className="category-icon">{category.icon}</div>
                <h3>{category.title}</h3>
                <p>{category.courseCount}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="page home-cta-section">
        <motion.div
          className="home-cta"
          initial={{ opacity: 0, scale: 0.94 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.55 }}
        >
          <div>
            <span className="cta-label">Start discovering</span>
            <h2>Ready to find your ideal course?</h2>
            <p>
              Enter your interests and receive recommendations created
              especially for you.
            </p>
          </div>

          <Link to="/recommendations" className="cta-button">
            Find My Courses
            <FaArrowRight />
          </Link>
        </motion.div>
      </section>
    </div>
  );
}

export default Home;