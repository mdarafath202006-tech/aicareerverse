import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { RiBrainLine } from "react-icons/ri";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-dark-900 flex flex-col items-center justify-center text-center p-6">
      <motion.div initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} className="space-y-6">
        <div className="w-20 h-20 rounded-3xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mx-auto">
          <RiBrainLine className="text-brand-300 text-4xl" />
        </div>
        <h1 className="font-display font-bold text-8xl text-white">404</h1>
        <p className="text-slate-400 max-w-sm">This page doesn't exist in the CareerVerse.</p>
        <Link to="/" className="btn-primary px-8 py-3 inline-flex">Go Home</Link>
      </motion.div>
    </div>
  );
}
