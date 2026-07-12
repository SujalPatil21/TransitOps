import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import truckImg from '../../assets/truck.png';
import { hasPlayedIntro, markIntroPlayed } from '../../utils/introAnimation';
import '../../styles/landing.css';

/**
 * LandingPage - Cinematic portal screen.
 * Plays the Right-to-Left driving animation exactly once per session,
 * then immediately redirects the user to the Login page.
 */
const LandingPage = () => {
  const navigate = useNavigate();
  
  // Show intro only if it hasn't been played in this browser session
  const [showIntro, setShowIntro] = useState(() => {
    return !hasPlayedIntro();
  });

  useEffect(() => {
    if (showIntro) {
      const timer = setTimeout(() => {
        setShowIntro(false);
        markIntroPlayed();
        navigate('/login');
      }, 4000); // 4.0s cinematic timeline unmount & redirect
      return () => clearTimeout(timer);
    } else {
      // If intro has already played, instantly redirect to /login
      navigate('/login');
    }
  }, [showIntro, navigate]);

  return (
    <div className="min-h-screen bg-bg-cream flex items-center justify-center overflow-hidden">
      {showIntro && (
        <div className="intro-overlay" aria-hidden="true">
          <div className="intro-truck-container">
            <img 
              src={truckImg} 
              alt="Driving Truck Illustration" 
              className="w-full h-auto object-contain" 
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default LandingPage;
