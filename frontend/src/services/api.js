import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

export const getCourses = async () => {
  try {
    const response = await api.get("/courses/");
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
        error.message ||
        "Unable to load courses."
    );
  }
};

export const getCourseById = async (courseId) => {
  try {
    const response = await api.get(`/courses/${courseId}`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
        error.message ||
        "Unable to load the course."
    );
  }
};

export const createCourse = async (courseData) => {
  try {
    const response = await api.post("/courses/", courseData);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
        error.message ||
        "Unable to create the course."
    );
  }
};

export const updateCourse = async (courseId, courseData) => {
  try {
    const response = await api.put(`/courses/${courseId}`, courseData);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
        error.message ||
        "Unable to update the course."
    );
  }
};

export const deleteCourse = async (courseId) => {
  try {
    const response = await api.delete(`/courses/${courseId}`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
        error.message ||
        "Unable to delete the course."
    );
  }
};

export const getStudents = async () => {
  try {
    const response = await api.get("/students/");
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
      error.message ||
      "Unable to load students."
    );
  }
};

export const getRecommendations = async (studentId) => {
  try {
    const response = await api.get(
      `/recommendations/${studentId}`
    );
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail ||
      error.message ||
      "Unable to generate recommendations."
    );
  }
};

export const createStudent = async (student) => {
  const response = await api.post("/students/", student);
  return response.data;
};

export default api;