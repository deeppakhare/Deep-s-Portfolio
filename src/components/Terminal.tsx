import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'motion/react';
import { Terminal } from 'lucide-react';

export default function TerminalSection() {
  const { t } = useTranslation();
  const [input, setInput] = useState('');
  const [output, setOutput] = useState<{ type: 'cmd' | 'text'; text: string }[]>([
    { type: 'text', text: 'Welcome to DeepOS v1.0.0' },
    { type: 'text', text: "Type 'help' to see available commands." }
  ]);
  const containerRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  if (containerRef.current) {
    containerRef.current.scrollTop = containerRef.current.scrollHeight;
  }
}, [output]);

  const handleCommand = (cmd: string) => {
    const cleanCmd = cmd.trim().toLowerCase();
    
    // Add command to output
    setOutput(prev => [...prev, { type: 'cmd', text: `guest@deep-portfolio:~$ ${cleanCmd}` }]);

    // Determine response
    let response = '';
    switch(cleanCmd) {
      case 'help':
        response = 'Available commands: about, skills, projects, contact, clear';
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
    <section className="py-24 relative px-6 z-10">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl font-display font-bold text-white flex items-center justify-center gap-3">
            <Terminal size={32} className="text-[#9d4edd]" /> {t('terminal.title')}
          </h2>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="rounded-xl overflow-hidden glass-panel border border-[#9d4edd]/30 shadow-[0_0_30px_rgba(157,78,221,0.15)] backdrop-blur-xl"
        >
          {/* Terminal Window Header */}
          <div className="bg-[#1a1b26]/80 px-4 py-3 flex items-center border-b border-white/10">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <div className="w-3 h-3 rounded-full bg-green-500" />
            </div>
            <div className="flex-1 text-center text-xs text-white/50 font-mono">guest@deep-terminal:~</div>
          </div>

          {/* Terminal Body */}
          <div ref={containerRef} className="bg-[#1a1b26]/50 p-6 font-mono text-sm h-80 overflow-y-auto custom-scrollbar">
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
              <span className="mr-2">guest@deep-terminal:~$</span>
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 bg-transparent outline-none border-none text-[#a9b1d6]"
                // autoFocus
                autoComplete="off"
                spellCheck="false"
              />
            </form>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
