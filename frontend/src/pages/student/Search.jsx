/**
 * pages/student/Search.jsx — Search Alumni
 */
import { useState } from "react";
import { motion } from "framer-motion";
import { RiSearchLine, RiBriefcaseLine, RiMapPinLine, RiLinkedinBoxLine, RiTeamLine } from "react-icons/ri";
import Layout from "../../components/Layout";
import toast from "react-hot-toast";

export default function AlumniSearch() {
  const [query, setQuery]   = useState("");
  const [skill, setSkill]   = useState("");
  const [company, setCompany] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const search = async () => {
    setLoading(true); setSearched(true);
    try {
      const params = new URLSearchParams({ q: query, skill, company });
      const r = await fetch(`/student/search?${params}`);
      const html = await r.text();
      // Parse JSON from API endpoint instead
      const apiR = await fetch(`/api/alumni?${params}`).catch(() => null);
      if (apiR?.ok) {
        const data = await apiR.json();
        setResults(data.alumni || []);
      } else {
        // Fallback: hit the backend
        setResults([]);
      }
    } catch { toast.error("Search failed"); }
    finally { setLoading(false); }
  };

  return (
    <Layout>
      <div className="p-6 max-w-5xl mx-auto space-y-6">
        <motion.div initial={{ opacity:0, y:-10 }} animate={{ opacity:1, y:0 }}>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-8 h-8 rounded-xl bg-accent-cyan/15 flex items-center justify-center">
              <RiSearchLine className="text-cyan-300" />
            </div>
            <h1 className="font-display font-bold text-2xl text-white">Browse Alumni</h1>
          </div>
          <p className="text-slate-400 text-sm ml-11">Search by name, skill, or company</p>
        </motion.div>

        {/* Search bar */}
        <motion.div initial={{ opacity:0 }} animate={{ opacity:1 }} transition={{ delay:0.1 }} className="card p-5">
          <div className="flex flex-col md:flex-row gap-3">
            <div className="relative flex-1">
              <RiSearchLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <input type="text" value={query} onChange={e => setQuery(e.target.value)}
                onKeyDown={e => e.key === "Enter" && search()}
                className="input pl-10" placeholder="Search by name or role..." />
            </div>
            <div className="relative">
              <input type="text" value={skill} onChange={e => setSkill(e.target.value)}
                className="input w-40" placeholder="Skill filter..." />
            </div>
            <div className="relative">
              <input type="text" value={company} onChange={e => setCompany(e.target.value)}
                className="input w-40" placeholder="Company..." />
            </div>
            <button onClick={search} disabled={loading} className="btn-primary px-6">
              {loading ? "Searching..." : "Search"}
            </button>
          </div>
        </motion.div>

        {/* Results */}
        {searched && !loading && (
          <motion.div initial={{ opacity:0 }} animate={{ opacity:1 }}>
            {results.length === 0 ? (
              <div className="card p-12 text-center">
                <RiTeamLine className="text-slate-600 text-4xl mx-auto mb-3" />
                <p className="text-slate-400">No alumni found. Try different search terms.</p>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 gap-4">
                {results.map((alum, i) => (
                  <motion.div
                    key={alum.id}
                    initial={{ opacity:0, y:16 }}
                    animate={{ opacity:1, y:0 }}
                    transition={{ delay: i * 0.05 }}
                    className="card-hover p-5"
                  >
                    <div className="flex gap-4">
                      <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-600 to-accent-violet flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                        {alum.name?.[0]?.toUpperCase()}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-display font-semibold text-white">{alum.name}</h3>
                        <div className="flex items-center gap-1.5 text-xs text-slate-400 mt-0.5">
                          <RiBriefcaseLine className="flex-shrink-0" />
                          <span className="truncate">{alum.job_role} {alum.company && `@ ${alum.company}`}</span>
                        </div>
                        {alum.location && (
                          <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-0.5">
                            <RiMapPinLine className="flex-shrink-0" /> {alum.location}
                          </div>
                        )}
                      </div>
                    </div>
                    {alum.skills && (
                      <div className="flex flex-wrap gap-1.5 mt-3">
                        {alum.skills.split(",").slice(0,4).map(s => (
                          <span key={s} className="badge-brand text-[10px]">{s.trim()}</span>
                        ))}
                      </div>
                    )}
                    <div className="flex gap-2 mt-4">
                      {alum.linkedin && (
                        <a href={alum.linkedin} target="_blank" rel="noopener noreferrer" className="btn-ghost btn-sm">
                          <RiLinkedinBoxLine className="text-blue-400" /> LinkedIn
                        </a>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </div>
    </Layout>
  );
}
