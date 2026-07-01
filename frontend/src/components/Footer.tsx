export default function Footer() {
  return (
    <footer className="mt-auto border-t border-slate-900 bg-[#04060b]/90 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <span className="font-display font-bold text-lg text-white">RideSphere</span>
          <p className="text-sm text-slate-500 mt-1">
            Enterprise-Grade Multi-Vehicle Rental & Tourism Ecosystem.
          </p>
        </div>
        <div className="flex space-x-6 text-sm text-slate-400">
          <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
          <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
          <a href="#" className="hover:text-white transition-colors">Contact Support</a>
        </div>
        <div className="text-xs text-slate-600">
          &copy; {new Date().getFullYear()} RideSphere Inc. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
