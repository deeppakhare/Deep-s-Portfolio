import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'motion/react';
import { ArrowDown, Github, Linkedin, Mail, Download } from 'lucide-react';
import FloatingLaptopContainer from './FloatingLaptop';
import TerminalModal from './TerminalModal';

export default function Hero() {
  const { t } = useTranslation();
  const [text, setText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);
  const [loopNum, setLoopNum] = useState(0);
  const [typingSpeed, setTypingSpeed] = useState(150);
  const [isTerminalOpen, setIsTerminalOpen] = useState(false);

  const roles = ["MERN Developer", "AI Enthusiast", "Frontend Engineer", "Tech Innovator"];

  useEffect(() => {
    let ticker = setTimeout(() => {
      handleTyping();
    }, typingSpeed);
    return () => clearTimeout(ticker);
  }, [text, isDeleting]);

  const handleTyping = () => {
    const i = loopNum % roles.length;
    const fullText = roles[i];

    setText(isDeleting ? fullText.substring(0, text.length - 1) : fullText.substring(0, text.length + 1));

    setTypingSpeed(isDeleting ? 30 : 150);

    if (!isDeleting && text === fullText) {
      setTimeout(() => setIsDeleting(true), 1500);
    } else if (isDeleting && text === '') {
      setIsDeleting(false);
      setLoopNum(loopNum + 1);
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center pt-24 pb-12 px-6">
      <div className="max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-8 items-center z-10">
        
        {/* LEFT SIDE: Content */}
        <div className="text-left relative z-10 order-2 lg:order-1 flex flex-col items-start pt-10 lg:pt-0">
          {/* Glow behind text */}
          <div className="absolute top-1/2 left-0 -translate-y-1/2 w-64 h-64 bg-[#9d4edd] blur-[120px] rounded-full opacity-30 pointer-events-none" />
          
          <motion.p 
            className="text-white/60 font-mono tracking-widest text-sm md:text-base uppercase mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            {t('hero.greeting')}
          </motion.p>
          
          <motion.h1 
            className="text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-display font-bold mb-4 tracking-tight text-white leading-tight"
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1, type: "spring" }}
          >
            Deep <br/> <span className="text-gradient">Pakhare</span>
          </motion.h1>

          <motion.div 
            className="h-10 md:h-12 mb-8 flex items-center font-mono text-lg md:text-2xl text-white/90"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.8 }}
          >
            <span className="mr-3 text-[#9d4edd]">&gt;</span>
            <span>{text}</span>
            <span className="animate-pulse ml-1 inline-block w-3 h-6 md:w-4 md:h-7 bg-[#9d4edd] translate-y-0.5"></span>
          </motion.div>
          
          <motion.p
            className="text-white/60 max-w-md text-base md:text-lg mb-10 leading-relaxed"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.8 }}
          >
            I build futuristic web experiences, robust AI systems, and modern SaaS applications. Exploring the intersection of design, code, and artificial intelligence.
          </motion.p>

          <motion.div 
            className="flex flex-col sm:flex-row items-center gap-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.8 }}
          >
            <a href="#projects" className="px-8 py-3.5 rounded-full bg-white text-black font-semibold hover:scale-105 hover:shadow-[0_0_20px_rgba(255,255,255,0.4)] transition-all flex items-center justify-center">
              {t('hero.cta')}
            </a>
            <a href="/resume/deep_resume.pdf" download className="px-8 py-3.5 rounded-full glass-panel border border-white/20 text-white font-medium hover:border-[#9d4edd]/50 hover:bg-[#9d4edd]/10 transition-colors flex items-center justify-center gap-2 group">
              <Download size={18} className="text-white/70 group-hover:text-[#9d4edd] transition-colors" />
              Resume
            </a>
          </motion.div>
          
          <motion.div 
            className="flex gap-4 mt-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 0.8 }}
          >
            <a href="https://github.com/deeppakhare19" aria-label="GitHub Profile" target="_blank" rel="noopener noreferrer" className="w-12 h-12 rounded-full glass-panel flex items-center justify-center text-white/70 hover:text-[#e0c3fc] hover:border-[#9d4edd]/50 transition-colors hover:shadow-[0_0_15px_rgba(157,78,221,0.3)]">
              <Github size={20} aria-hidden="true" />
            </a>
            <a href="https://linkedin.com/in/deeppakhare19" aria-label="LinkedIn Profile" target="_blank" rel="noopener noreferrer" className="w-12 h-12 rounded-full glass-panel flex items-center justify-center text-white/70 hover:text-[#e0c3fc] hover:border-[#9d4edd]/50 transition-colors hover:shadow-[0_0_15px_rgba(157,78,221,0.3)]">
              <Linkedin size={20} aria-hidden="true" />
            </a>
          </motion.div>
        </div>
        
        {/* RIGHT SIDE: 3D Laptop */}
        <motion.div 
          className="h-[50vh] lg:h-[80vh] w-full relative order-1 lg:order-2"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.5, delay: 0.2, ease: "easeOut" }}
        >
           <FloatingLaptopContainer onLaptopClick={() => setIsTerminalOpen(true)} />
        </motion.div>
      </div>

      <motion.div 
        className="absolute bottom-6 left-1/2 -translate-x-1/2 text-white/30 animate-bounce cursor-pointer hover:text-white transition-colors"
        onClick={() => document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' })}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 1 }}
      >
        <ArrowDown size={24} />
      </motion.div>
      
      <TerminalModal isOpen={isTerminalOpen} onClose={() => setIsTerminalOpen(false)} />
    </section>
  );
}
