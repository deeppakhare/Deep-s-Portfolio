import React, { Suspense, useEffect } from 'react';
import Navbar from './components/Navbar';
import ParticleCursor from './components/ParticleCursor';
import MusicPlayer from './components/MusicPlayer';
import Hero from './components/Hero';
import About from './components/About';
import Skills from './components/Skills';
import Projects from './components/Projects';
import Experience from './components/Experience';
import GitHubSection from './components/GitHubSection';
import TerminalSection from './components/Terminal';
import Contact from './components/Contact';
import Scene3D from './components/Scene3D';
import './i18n';

export default function App() {
    useEffect(() => {
    // Prevent browser from restoring scroll position
    if ('scrollRestoration' in history) {
      history.scrollRestoration = 'manual';
    }
    // Force scroll to top
    window.scrollTo(0, 0);
  }, []);
  return (
    <div className="relative min-h-screen bg-[#050505] selection:bg-[#9d4edd]/30 selection:text-white">
      {/* Background and Cursor */}
      <ParticleCursor />
      
      <Suspense fallback={<div className="fixed inset-0 bg-[#050505] flex items-center justify-center text-white">Loading Experience...</div>}>
        <Scene3D />
      </Suspense>

      {/* Floating Elements */}
      <Navbar />
      <MusicPlayer />

      {/* Main Content Sections */}
      <main className="relative">
        <Hero />
        <About />
        <Skills />
        <Projects />
        <Experience />
        <GitHubSection />
        <TerminalSection />
        <Contact />
      </main>
    </div>
  );
}
