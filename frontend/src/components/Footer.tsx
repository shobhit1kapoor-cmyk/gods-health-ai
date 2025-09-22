import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Activity } from 'lucide-react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    info: [
      { name: 'About', href: '/about' },
    ],
  };

  // Removed inaccessible social links

  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="container-max px-4 sm:px-6 lg:px-8 section-padding">
        <div className="py-12">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Brand Section */}
            <div>
              <Link to="/" className="flex items-center space-x-2 mb-4">
                <div className="relative">
                  <Heart className="h-8 w-8 text-primary-600" />
                  <Activity className="h-4 w-4 text-primary-400 absolute -top-1 -right-1" />
                </div>
                <span className="text-xl font-display font-bold gradient-text">
                  Gods Health AI
                </span>
              </Link>
              <p className="text-gray-600 mb-6 max-w-md">
                Advanced AI-powered health prediction platform providing comprehensive risk assessments 
                and personalized health insights to empower better healthcare decisions.
              </p>
              {/* Removed GitHub logo and other social links as they were inaccessible */}
            </div>

            {/* Removed Product Links section as they were inaccessible */}

            {/* Info Links */}
            <div>
              <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">
                Info
              </h3>
              <ul className="space-y-3">
                {footerLinks.info.map((link) => (
                  <li key={link.name}>
                    <Link
                      to={link.href}
                      className="text-gray-600 hover:text-primary-600 transition-colors duration-200"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>


          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-200 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-500 text-sm">
              © {currentYear} Gods Health AI. Made by Shobhit Kapoor.
            </p>
            <div className="flex items-center space-x-6 mt-4 md:mt-0">
              <p className="text-xs text-gray-400">
                ⚠️ For informational purposes only. Not a substitute for professional medical advice.
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;