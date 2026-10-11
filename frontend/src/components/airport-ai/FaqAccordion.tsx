import React, { useState, useEffect } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, Tag } from 'lucide-react';
import { FAQItem } from '../../types';
import { api } from '../../services/api';

interface FaqAccordionProps {
  language: string;
}

export const FaqAccordion: React.FC<FaqAccordionProps> = ({ language }) => {
  const [faqs, setFaqs] = useState<FAQItem[]>([]);
  const [openId, setOpenId] = useState<number | null>(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFaqs = async () => {
      setLoading(true);
      try {
        const data = await api.getFaqs(language);
        setFaqs(data.faqs);
      } catch (err) {
        console.error('Failed to load FAQs', err);
      } finally {
        setLoading(false);
      }
    };
    fetchFaqs();
  }, [language]);

  return (
    <div className="bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-[#1E2E4E]">
        <div className="flex items-center space-x-2.5">
          <HelpCircle className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-white text-base">Airport FAQs Knowledge Hub</h3>
        </div>
        <span className="text-xs text-cyan-400 font-mono bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800">
          {language.toUpperCase()}
        </span>
      </div>

      {loading ? (
        <div className="text-center py-8 text-slate-400 text-xs">Loading localized FAQs...</div>
      ) : (
        <div className="space-y-2.5 max-h-[420px] overflow-y-auto pr-1">
          {faqs.map((faq) => {
            const isOpen = openId === faq.id;
            return (
              <div
                key={faq.id}
                className="bg-[#121E3B] border border-[#22355A] rounded-xl overflow-hidden transition-all shadow-sm"
              >
                <button
                  onClick={() => setOpenId(isOpen ? null : faq.id)}
                  className="w-full px-4 py-3 text-left flex items-center justify-between space-x-3 hover:bg-[#162547] transition-colors"
                >
                  <div className="flex items-center space-x-2.5">
                    <span className="text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-cyan-400 px-2 py-0.5 rounded border border-slate-700">
                      {faq.category}
                    </span>
                    <span className="text-xs font-semibold text-white">{faq.question}</span>
                  </div>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-cyan-400 shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                  )}
                </button>

                {isOpen && (
                  <div className="px-4 pb-4 pt-1 border-t border-slate-800/80 space-y-2">
                    <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-line">{faq.answer}</p>
                    <div className="flex items-center space-x-1.5 text-[10px] text-slate-400 pt-1">
                      <Tag className="w-3 h-3 text-slate-500" />
                      <span>Keywords: {faq.keywords}</span>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
