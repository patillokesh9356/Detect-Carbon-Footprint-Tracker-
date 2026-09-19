import { useState, useEffect } from "react";
import "./App.css";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

function App() {
  // =========================
  // LOGIN / REGISTER STATES
  // =========================

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [authMessage, setAuthMessage] = useState("");

  const [loggedUser, setLoggedUser] = useState(null);

  // =========================
  // ACTIVITY STATES
  // =========================

  // Auto-unit mapping per category
  const categoryUnits = {
    electricity: "kWh",
    petrol: "liters",
    diesel: "liters",
    car: "km",
    bus: "km",
    train: "km",
  };

  const [category, setCategory] = useState("electricity");
  const [value, setValue] = useState("");
  const [unit, setUnit] = useState("kWh");
  const [date, setDate] = useState("2026-09-15");

  // Auto-update unit when category changes
  const handleCategoryChange = (e) => {
    const newCategory = e.target.value;
    setCategory(newCategory);
    setUnit(categoryUnits[newCategory] || "");
  };

  const [result, setResult] = useState("");
  const [totalEmission, setTotalEmission] = useState(0);
  const [monthlyData, setMonthlyData] = useState([]);
  const [activities, setActivities] = useState([]);
  const [goals, setGoals] = useState([]);

  // =========================
  // GOAL FORM STATES
  // =========================
  const [targetReduction, setTargetReduction] = useState("");
  const [goalStartDate, setGoalStartDate] = useState("");
  const [goalEndDate, setGoalEndDate] = useState("");
  const [goalMessage, setGoalMessage] = useState("");
  const API = import.meta.env.VITE_BACKEND_URL;

  // =========================
  // LOGIN
  // =========================

  const handleLogin = async () => {
    if (!email || !password) {
      setAuthMessage("Please enter email and password.");
      return;
    }

    try {
      const response = await fetch(`${API}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setIsLoggedIn(true);
        setLoggedUser(data);

        setAuthMessage("");
        setPassword("");

        setEmail("");
      } else {
        setAuthMessage(data.error);
      }
    } catch (error) {
      setAuthMessage("Backend server is not running.");
    }
  };

  // =========================
  // REGISTER
  // =========================

  const handleRegister = async () => {
    if (!name || !email || !password) {
      setAuthMessage("Please fill all fields.");
      return;
    }

    try {
      const response = await fetch(`${API}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setAuthMessage("Registration successful! Please login.");

        setName("");
        setEmail("");
        setPassword("");

        setShowRegister(false);
      } else {
        setAuthMessage(data.error);
      }
    } catch (error) {
      setAuthMessage("Backend server is not running.");
    }
  };

  // =========================
  // GET TOTAL EMISSION
  // =========================

  const getTotalEmission = async (userId) => {
    try {
      const response = await fetch(
        `${API}/total-emission/${userId}`,
      );

      const data = await response.json();

      if (response.ok) {
        setTotalEmission(data.total_emission);
      }
    } catch (error) {
      console.log("Could not fetch total emission");
    }
  };

  // =========================
  // GET MONTHLY EMISSION
  // =========================

  const getMonthlyEmission = async (userId) => {
    try {
      const response = await fetch(
        `${API}/monthly-emission/${userId}`,
      );

      const data = await response.json();

      if (response.ok) {
        setMonthlyData(data.monthly_emission);
      }
    } catch (error) {
      console.log("Could not fetch monthly emission");
    }
  };

  // =========================
  // GET ACTIVITIES
  // =========================

  const getActivities = async (userId) => {
    try {
      const response = await fetch(
        `${API}/activities/${userId}`,
      );

      const data = await response.json();

      if (response.ok) {
        setActivities(data.activities);
      }
    } catch (error) {
      console.log("Could not fetch activities");
    }
  };
  // =========================
  // GET USER GOALS
  // =========================

  const getGoals = async (userId) => {
    try {
      const response = await fetch(`${API}/goals/${userId}`);

      const data = await response.json();

      if (response.ok) {
        setGoals(data.goals);
      }
    } catch (error) {
      console.log("Could not fetch goals");
    }
  };
  // =========================
  // ADD GOAL
  // =========================

  const addGoal = async () => {
    if (!targetReduction || !goalStartDate || !goalEndDate) {
      setGoalMessage("Please fill all goal fields.");
      return;
    }

    try {
      const response = await fetch(`${API}/goals`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: loggedUser.user_id,
          target_reduction: targetReduction,
          start_date: goalStartDate,
          end_date: goalEndDate,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setGoalMessage(`Goal added! Target: ${data.target_reduction}% reduction`);
        setTargetReduction("");
        setGoalStartDate("");
        setGoalEndDate("");
        getGoals(loggedUser.user_id);
      } else {
        setGoalMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setGoalMessage("Backend server is not running.");
    }
  };

  // =========================
  // LOAD USER DATA AFTER LOGIN
  // =========================

  useEffect(() => {
    if (isLoggedIn && loggedUser) {
      const userId = loggedUser.user_id;

      getTotalEmission(userId);
      getMonthlyEmission(userId);
      getActivities(userId);
      getGoals(userId);
    }
  }, [isLoggedIn, loggedUser]);

  // =========================
  // ADD ACTIVITY
  // =========================

  const addActivity = async () => {
    if (!value) {
      setResult("Please enter a value.");
      return;
    }

    try {
      const response = await fetch(`${API}/activities`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: loggedUser.user_id,
          category: category,
          value: value,
          unit: unit,
          activity_date: date,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(
          `Activity added successfully! Emission: ${data.emission} kg CO2e`,
        );

        setValue("");

        getTotalEmission(loggedUser.user_id);
        getMonthlyEmission(loggedUser.user_id);
        getActivities(loggedUser.user_id);
        getGoals(loggedUser.user_id);
      } else {
        setResult(`Error: ${data.error}`);
      }
    } catch (error) {
      setResult("Backend server is not running.");
    }
  };

  // =========================
  // LOGOUT
  // =========================

  const handleLogout = () => {
    setIsLoggedIn(false);
    setLoggedUser(null);

    setTotalEmission(0);
    setMonthlyData([]);
    setActivities([]);

    setResult("");
    setAuthMessage("");
  };

  // =========================
  // CHART
  // =========================

  const chartData = {
    labels: monthlyData.map((item) => item.month),

    datasets: [
      {
        label: "Carbon Emission (kg CO2e)",
        data: monthlyData.map((item) => item.total_emission),
        tension: 0.3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,

    plugins: {
      legend: {
        display: true,
      },

      title: {
        display: true,
        text: "Monthly Carbon Emission",
      },
    },
  };

  // =========================
  // LOGIN / REGISTER PAGE
  // =========================

  if (!isLoggedIn) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <h1>🌱 Carbon Footprint Tracker</h1>

          <p className="auth-subtitle">
            Track your emissions and build a greener future.
          </p>

          {showRegister ? (
            <>
              <h2>Create Account</h2>

              <input
                type="text"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />

              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <button className="auth-button" onClick={handleRegister}>
                Register
              </button>

              <p className="switch-text">
                Already have an account?
                <button
                  className="link-button"
                  onClick={() => {
                    setShowRegister(false);
                    setAuthMessage("");
                  }}
                >
                  Login
                </button>
              </p>
            </>
          ) : (
            <>
              <h2>Login</h2>

              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <button className="auth-button" onClick={handleLogin}>
                Login
              </button>

              <p className="switch-text">
                Don't have an account?
                <button
                  className="link-button"
                  onClick={() => {
                    setShowRegister(true);
                    setAuthMessage("");
                  }}
                >
                  Register
                </button>
              </p>
            </>
          )}

          {authMessage && <div className="auth-message">{authMessage}</div>}
        </div>
      </div>
    );
  }

  // =========================
  // DASHBOARD
  // =========================

  return (
    <div className="app-container">
      <div className="header">
        <h1>🌱 Carbon Footprint Tracker</h1>

        <p>
          Welcome, <strong>{loggedUser.name}</strong>!
        </p>

        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div className="dashboard-card">
        <h3>Total Carbon Emission</h3>
        <div className="total-emission">{totalEmission} kg CO2e</div>
        <p>Your current recorded carbon footprint</p>
      </div>

      <div className="section">
        <h2>➕ Add Activity</h2>

        <div className="form-grid">
          <div className="form-group">
            <label>Activity Category</label>
            <select value={category} onChange={handleCategoryChange}>
              <option value="electricity">Electricity</option>
              <option value="petrol">Petrol</option>
              <option value="diesel">Diesel</option>
              <option value="car">Car</option>
              <option value="bus">Bus</option>
              <option value="train">Train</option>
            </select>
          </div>
          <div className="form-group">
            <label>Value</label>
            <input
              type="number"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              placeholder="Enter value"
            />
          </div>
          <div className="form-group">
            <label>Unit</label>
            <input
              type="text"
              value={unit}
              onChange={(e) => setUnit(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
        </div>

        <button className="add-button" onClick={addActivity}>
          Add Activity
        </button>

        {result && <div className="result">{result}</div>}
      </div>

      <div className="section">
        <h2>🎯 Reduction Goals</h2>

        <div className="form-grid">
          <div className="form-group">
            <label>Target Reduction (%)</label>
            <input
              type="number"
              min="1"
              max="100"
              placeholder="e.g. 20"
              value={targetReduction}
              onChange={(e) => setTargetReduction(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Start Date</label>
            <input
              type="date"
              value={goalStartDate}
              onChange={(e) => setGoalStartDate(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>End Date</label>
            <input
              type="date"
              value={goalEndDate}
              onChange={(e) => setGoalEndDate(e.target.value)}
            />
          </div>
        </div>

        <button className="add-button" onClick={addGoal}>
          Add Goal
        </button>

        {goalMessage && <div className="result">{goalMessage}</div>}

        <h3 style={{ marginTop: "24px" }}>📋 Goal History</h3>

        {goals.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Target Reduction</th>
                  <th>Start Date</th>
                  <th>End Date</th>
                </tr>
              </thead>
              <tbody>
                {goals.map((goal) => (
                  <tr key={goal.id}>
                    <td>{goal.target_reduction}%</td>
                    <td>{goal.start_date}</td>
                    <td>{goal.end_date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No goals added yet.</p>
        )}
      </div>

      <div className="section">
        <h2>📊 Monthly Emission</h2>

        <div className="chart-container">
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>

      <div className="section">
        <h2>📋 Activity History</h2>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Value</th>
                <th>Unit</th>
                <th>Emission</th>
                <th>Date</th>
              </tr>
            </thead>

            <tbody>
              {activities.map((activity) => (
                <tr key={activity.id}>
                  <td>{activity.category}</td>

                  <td>{activity.activity_value}</td>

                  <td>{activity.unit}</td>

                  <td>{activity.emission} kg CO2e</td>

                  <td>
                    {new Date(activity.activity_date).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
    <footer style={{
      textAlign: "center",
      padding: "16px",
      marginTop: "32px",
      color: "#888",
      fontSize: "14px",
      borderTop: "1px solid #e0e0e0"
    }}>
      Developed by <strong>Lokesh Patil</strong>
    </footer>
  </div>
  );
}

export default App;
