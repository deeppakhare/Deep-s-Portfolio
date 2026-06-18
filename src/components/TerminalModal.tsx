import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, Terminal } from 'lucide-react';

interface TerminalModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function TerminalModal({ isOpen, onClose }: TerminalModalProps) {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState<{ type: 'cmd' | 'text'; text: string }[]>([
    { type: 'text', text: 'Welcome to DeepOS v1.0.0 (Interactive Mode)' },
    { type: 'text', text: "Type 'help' to see available commands. Type 'exit' to close." }
  ]);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

 useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
      if (containerRef.current) {
        containerRef.current.scrollTop = containerRef.current.scrollHeight;
      }
    }
  }, [isOpen, output]);

  const handleCommand = (cmd: string) => {
    const cleanCmd = cmd.trim().toLowerCase();
    
    setOutput(prev => [...prev, { type: 'cmd', text: `guest@deep-portfolio:~$ ${cleanCmd}` }]);

    let response = '';
    switch(cleanCmd) {
      case 'help':
        response = 'Available commands: about, skills, projects, contact, clear, exit';
        break;
      case 'about':
        response = 'Deep Pakhare - MERN Developer, AI Enthusiast, B.Tech CSE student from Maharashtra, India.\nBuilding solutions that matter.';
        break;
      case 'skills':
        response = '> Frontend: React, Javascript, Tailwind, Three.js\n> Backend: Node.js, MongoDB\n> Tools: Git, Figma, AI Studio';
        break;
      case 'projects':
        response = '1. Civic Issue Reporting App\n2. Shroomify\n3. Deep-s-Portfolio';
        break;
      case 'contact':
        response = 'Email: deeppakhare19@gmail.com\nGitHub: github.com/deeppakhare\nLinkdin: www.linkedin.com/in/deeppakhare6669';
        break;
      case 'exit':
        onClose();
        return;
      case 'clear':
        setOutput([]);
        return;
      case '':
        return;
      default:
        response = `Command not found: ${cleanCmd}. Type 'help' for available commands.`;
    }

    setOutput(prev => [...prev, { type: 'text', text: response }]);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 md:p-12"
          onClick={onClose}
        >
          {/* Backdrop Blur */}
          <div className="absolute inset-0 bg-black/60 backdrop-blur-md" />

          {/* Terminal Window */}
          <motion.div 
            initial={{ scale: 0.9, y: 20, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.9, y: 20, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="relative w-full max-w-4xl h-[80vh] md:h-[70vh] rounded-2xl overflow-hidden glass-panel border border-[#9d4edd]/50 shadow-[0_0_50px_rgba(157,78,221,0.2)] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="bg-[#0f0f13]/90 px-4 py-3 flex items-center border-b border-white/10 shrink-0">
              <div className="flex gap-2">
                <button onClick={onClose} className="w-3 h-3 rounded-full bg-red-500 hover:bg-red-400 transition-colors" />
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <div className="w-3 h-3 rounded-full bg-green-500" />
              </div>
              <div className="flex-1 text-center flex justify-center items-center gap-2 text-sm text-white/60 font-mono">
                <Terminal size={14} className="text-[#9d4edd]" />
                deep-os-terminal
              </div>
              <button onClick={onClose} className="text-white/40 hover:text-white transition-colors">
                <X size={18} />
              </button>
            </div>

            {/* Body */}
            <div ref={containerRef} className="bg-[#1a1b26]/80 p-6 font-mono text-sm sm:text-base flex-1 overflow-y-auto custom-scrollbar" onClick={() => inputRef.current?.focus()}>
              {output.map((line, i) => (
                <div key={i} className={`mb-2 ${line.type === 'cmd' ? 'text-[#e0c3fc]' : 'text-[#a9b1d6] whitespace-pre-wrap leading-relaxed'}`}>
                  {line.text}
                </div>
              ))}
              
              <form 
                onSubmit={(e) => {
                  e.preventDefault();
                  handleCommand(input);
                  setInput('');
                }}
                className="flex items-center text-[#e0c3fc] mt-2"
              >
                <span className="mr-2 shrink-0">guest@deep-portfolio:~$</span>
                <input 
                  ref={inputRef}
                  type="text" 
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  className="flex-1 bg-transparent outline-none border-none text-[#a9b1d6] min-w-0"
                  // autoFocus
                  autoComplete="off"
                  spellCheck="false"
                />
              </form>
              <div className="h-4" />
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
