import { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

export default function InputArea({ onSendMessage, isLoading }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="p-4 bg-slate-900/80 backdrop-blur-md border-t border-slate-800">
      <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything..."
          disabled={isLoading}
          className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all disabled:opacity-50"
        />
        <button 
          type="submit" 
          disabled={isLoading || !input.trim()}
          className="bg-blue-600 p-3 rounded-xl hover:bg-blue-700 active:scale-95 transition-all disabled:opacity-50 disabled:hover:bg-blue-600 flex items-center justify-center min-w-[52px]"
        >
          {isLoading ? (
            <Loader2 className="animate-spin text-white" size={24} />
          ) : (
            <Send className="text-white" size={24} />
          )}
        </button>
      </form>
    </div>
  );
}
