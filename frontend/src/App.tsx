import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ThemeProvider } from './contexts/ThemeContext.tsx';
import Navbar from './components/Navbar.tsx';
import Home from './pages/Home.tsx';
import PredictorsList from './pages/PredictorsList.tsx';
import PredictorDetail from './pages/PredictorDetail.tsx';
import About from './pages/About.tsx';
import Footer from './components/Footer.tsx';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
          <Navbar />
          <motion.main 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="pt-16 px-4 sm:px-6 lg:px-8"
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/predictors" element={<PredictorsList />} />
              <Route path="/predictor/:predictorId" element={<PredictorDetail />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </motion.main>
          <Footer />
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;