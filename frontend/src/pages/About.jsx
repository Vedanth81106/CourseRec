import { motion } from "framer-motion";
import {
  FaBookOpen,
  FaBrain,
  FaBullseye,
  FaCheckCircle,
  FaCode,
  FaDatabase,
  FaLightbulb,
  FaReact,
  FaRocket,
  FaServer,
  FaUsers,
} from "react-icons/fa";

function About() {
  const steps = [
    {
      number: "01",
      title: "Enter your interests",
      description:
        "Tell CourseRec what subject, skill, or domain you would like to learn.",
    },
    {
      number: "02",
      title: "Apply useful filters",
      description:
        "Select your preferred difficulty level and course duration.",
    },
    {
      number: "03",
      title: "Explore recommendations",
      description:
        "View suitable courses and choose the one that best matches your goals.",
    },
  ];

  const benefits = [
    "Reduces the time spent searching for suitable courses",
    "Makes course discovery simple and student-friendly",
    "Helps learners compare courses based on useful details",
    "Supports more informed learning decisions",
  ];

  const technologies = [
    {
      icon: <FaReact />,
      name: "React",
      description: "Builds the interactive frontend interface.",
    },
    {
      icon: <FaCode />,
      name: "JavaScript",
      description: "Handles the application logic and user interactions.",
    },
    {
      icon: <FaServer />,
      name: "FastAPI",
      description: "Provides backend APIs and processes requests.",
    },
    {
      icon: <FaDatabase />,
      name: "Database",
      description: "Stores and manages available course information.",
    },
  ];

  return (
    <div className="about-page">
      <section className="about-hero">
        <div className="about-decoration about-decoration-one"></div>
        <div className="about-decoration about-decoration-two"></div>

        <div className="page about-hero-container">
          <motion.div
            className="about-hero-content"
            initial={{ opacity: 0, x: -35 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="about-eyebrow">About CourseRec</span>

            <h1>
              Helping students make smarter
              <span> learning decisions.</span>
            </h1>

            <p>
              CourseRec is a course recommendation platform designed to help
              students discover courses based on their interests, preferred
              learning level, and available time.
            </p>

            <div className="about-hero-points">
              <div>
                <FaCheckCircle />
                Easy to use
              </div>

              <div>
                <FaCheckCircle />
                Student focused
              </div>

              <div>
                <FaCheckCircle />
                Personalized results
              </div>
            </div>
          </motion.div>

          <motion.div
            className="about-hero-visual"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.15 }}
          >
            <div className="about-visual-card glass-card">
              <div className="about-visual-icon">
                <FaBrain />
              </div>

              <span>Course Recommendation System</span>

              <h3>Learn what suits you best</h3>

              <p>
                CourseRec connects student preferences with relevant course
                information to create a simpler learning discovery experience.
              </p>

              <div className="about-visual-stats">
                <div>
                  <strong>Simple</strong>
                  <span>Search process</span>
                </div>

                <div>
                  <strong>Smart</strong>
                  <span>Course filtering</span>
                </div>

                <div>
                  <strong>Useful</strong>
                  <span>Recommendations</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="page section about-purpose-section">
        <motion.div
          className="about-purpose-card glass-card"
          initial={{ opacity: 0, y: 35 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.25 }}
          transition={{ duration: 0.55 }}
        >
          <div className="about-purpose-icon">
            <FaBullseye />
          </div>

          <div>
            <span className="section-tag">Our purpose</span>

            <h2>Why was CourseRec created?</h2>

            <p>
              Students often have access to a large number of online courses,
              but choosing the right one can be confusing. CourseRec reduces
              this difficulty by organizing course information and helping
              users narrow down their options using clear preferences.
            </p>

            <p>
              The system aims to provide a convenient starting point for
              students who want to learn a new skill but are unsure which
              course best suits their requirements.
            </p>
          </div>
        </motion.div>
      </section>

      <section className="section how-it-works-section">
        <div className="page">
          <div className="section-heading">
            <span className="section-tag">How it works</span>

            <h2 className="section-title">
              Find suitable courses in three simple steps
            </h2>

            <p className="section-subtitle">
              CourseRec keeps the recommendation process straightforward and
              easy to understand.
            </p>
          </div>

          <div className="about-steps-grid">
            {steps.map((step, index) => (
              <motion.article
                key={step.number}
                className="about-step-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.25 }}
                transition={{
                  duration: 0.45,
                  delay: index * 0.12,
                }}
              >
                <span className="about-step-number">{step.number}</span>

                <div className="about-step-icon">
                  {index === 0 && <FaLightbulb />}
                  {index === 1 && <FaBookOpen />}
                  {index === 2 && <FaRocket />}
                </div>

                <h3>{step.title}</h3>
                <p>{step.description}</p>
              </motion.article>
            ))}
          </div>
        </div>
      </section>

      <section className="page section about-benefits-section">
        <div className="about-benefits-grid">
          <motion.div
            className="about-benefits-content"
            initial={{ opacity: 0, x: -35 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.55 }}
          >
            <span className="section-tag">Key benefits</span>

            <h2>Designed to make course selection easier</h2>

            <p>
              CourseRec provides a clear interface that helps students focus
              on the information that matters when selecting a course.
            </p>

            <div className="about-benefit-list">
              {benefits.map((benefit) => (
                <div key={benefit}>
                  <FaCheckCircle />
                  <span>{benefit}</span>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            className="about-benefits-visual"
            initial={{ opacity: 0, x: 35 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.55 }}
          >
            <div className="benefit-highlight-card">
              <FaUsers />

              <span>Built for students</span>

              <h3>A clear and friendly recommendation experience</h3>

              <p>
                The interface avoids unnecessary complexity and presents
                course details in a way that is easy to compare.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="section technology-section">
        <div className="page">
          <div className="section-heading">
            <span className="section-tag">Technology</span>

            <h2 className="section-title">Built using modern technologies</h2>

            <p className="section-subtitle">
              The project combines a responsive React frontend with a FastAPI
              backend and database support.
            </p>
          </div>

          <div className="technology-grid">
            {technologies.map((technology, index) => (
              <motion.article
                key={technology.name}
                className="technology-card glass-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{
                  duration: 0.45,
                  delay: index * 0.1,
                }}
              >
                <div className="technology-icon">{technology.icon}</div>

                <h3>{technology.name}</h3>

                <p>{technology.description}</p>
              </motion.article>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default About;