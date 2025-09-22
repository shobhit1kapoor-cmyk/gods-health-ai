import React from 'react';
import { motion } from 'framer-motion';
import {
  Heart,
  Brain,
  Shield,
  Users,
  Award,
  Target,
  Zap,
  CheckCircle,
  TrendingUp,
  Activity,
  Stethoscope,
  AlertTriangle
} from 'lucide-react';

const About: React.FC = () => {
  const features = [
    {
      icon: Brain,
      title: 'Advanced AI Technology',
      description: 'Our platform uses state-of-the-art machine learning algorithms trained on vast medical datasets to provide accurate health predictions.',
    },
    {
      icon: Shield,
      title: 'Privacy & Security',
      description: 'Your health data is encrypted and secure. We follow strict privacy protocols and never share your personal information.',
    },
    {
      icon: Users,
      title: 'Expert Validation',
      description: 'All our predictors are developed and validated by medical professionals and data scientists with years of experience.',
    },
    {
      icon: Target,
      title: 'Personalized Insights',
      description: 'Get tailored health recommendations based on your unique profile, medical history, and lifestyle factors.',
    },
  ];

  const stats = [
    { icon: Heart, label: 'Health Predictors', value: '22+', description: 'Comprehensive AI models' },
    { icon: Users, label: 'Accuracy Rate', value: '95%', description: 'Average prediction accuracy' },
    { icon: Activity, label: 'Data Points', value: '1000+', description: 'Medical parameters analyzed' },
    { icon: Award, label: 'Medical Conditions', value: '50+', description: 'Conditions covered' },
  ];

  const creator = {
    name: 'Shobhit Kapoor',
    role: 'Creator & Developer',
      description: 'Full-stack developer and AI enthusiast who created this comprehensive health prediction platform.',
      image: '/api/placeholder/150/150'
    },
  ];

  const predictorCategories = [
    {
      icon: Heart,
      title: 'Disease Risk & Diagnosis',
      count: 7,
      items: ['Heart Disease', 'Stroke Risk', 'Cancer Detection', 'Kidney Disease', 'Liver Disease', 'Alzheimer\'s', 'Parkinson\'s'],
      color: 'from-red-500 to-pink-500'
    },
    {
      icon: Activity,
      title: 'Condition & Complications',
      count: 5,
      items: ['Sepsis', 'Hospital Readmission', 'ICU Mortality', 'Post-Surgery', 'Pregnancy Complications'],
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: TrendingUp,
      title: 'Lifestyle & Prevention',
      count: 5,
      items: ['Obesity Risk', 'Hypertension', 'Cholesterol Risk', 'Mental Health', 'Sleep Apnea'],
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: Stethoscope,
      title: 'Specialized Care',
      count: 5,
      items: ['COVID-19 Risk', 'Asthma/COPD', 'Anemia', 'Thyroid Disorders', 'Cancer Recurrence'],
      color: 'from-purple-500 to-indigo-500'
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-br from-primary-50 to-indigo-100 dark:from-gray-800 dark:to-gray-900">
        <div className="container-max section-padding">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto"
          >
            <h1 className="text-4xl lg:text-6xl font-display font-bold text-gray-900 dark:text-white mb-6">
              About
              <span className="gradient-text block">
                Gods Health AI
              </span>
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
              A personal project revolutionizing healthcare through artificial intelligence, providing accurate health predictions 
              and personalized insights to help you make informed decisions about your health and wellness.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20">
        <div className="container-max section-padding">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-3xl lg:text-4xl font-display font-bold text-gray-900 dark:text-white mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
                To democratize access to advanced healthcare insights by leveraging artificial intelligence 
                to predict health risks, detect diseases early, and provide personalized recommendations 
                for better health outcomes.
              </p>
              <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
                We believe that everyone deserves access to cutting-edge health technology that can help 
                prevent diseases, improve quality of life, and ultimately save lives through early detection 
                and intervention.
              </p>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="grid grid-cols-2 gap-4">
                {stats.map((stat, index) => {
                  const Icon = stat.icon;
                  return (
                    <motion.div
                      key={stat.label}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: index * 0.1 }}
                      className="card text-center"
                    >
                      <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                        <Icon className="h-6 w-6 text-primary-600" />
                      </div>
                      <div className="text-2xl font-bold gradient-text mb-1">
                        {stat.value}
                      </div>
                      <div className="text-sm font-medium text-gray-900 mb-1">
                        {stat.label}
                      </div>
                      <div className="text-xs text-gray-500">
                        {stat.description}
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container-max section-padding">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl lg:text-4xl font-display font-bold text-gray-900 dark:text-white mb-4">
              What Makes Us Different
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Our platform combines cutting-edge AI technology with medical expertise 
              to deliver the most accurate and actionable health insights.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="card text-center group hover:shadow-large transition-all duration-300"
                >
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-200 transition-colors duration-300">
                    <Icon className="h-8 w-8 text-primary-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    {feature.description}
                  </p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Predictor Categories Section */}
      <section className="py-20">
        <div className="container-max section-padding">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl lg:text-4xl font-display font-bold text-gray-900 dark:text-white mb-4">
              Our Health Predictors
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Comprehensive AI-powered health predictions covering every aspect of your health journey.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {predictorCategories.map((category, index) => {
              const Icon = category.icon;
              return (
                <motion.div
                  key={category.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="card group hover:shadow-large transition-all duration-300"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`w-12 h-12 bg-gradient-to-br ${category.color} rounded-lg flex items-center justify-center`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <span className="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                      {category.count} Predictors
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                    {category.title}
                  </h3>
                  <div className="space-y-2">
                    {category.items.map((item, itemIndex) => (
                      <div key={itemIndex} className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        {item}
                      </div>
                    ))}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Creator Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container-max section-padding">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl lg:text-4xl font-display font-bold text-gray-900 dark:text-white mb-4">
              Creator
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              This project is made by Shobhit Kapoor
            </p>
          </motion.div>

          <div className="flex justify-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="card text-center group hover:shadow-large transition-all duration-300"
            >
              <div className="w-24 h-24 bg-gradient-to-br from-primary-400 to-indigo-500 rounded-full mx-auto mb-4 flex items-center justify-center">
                <Users className="h-12 w-12 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
                {creator.name}
              </h3>
              <p className="text-primary-600 dark:text-primary-400 font-medium mb-3">
                {creator.role}
              </p>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                {creator.description}
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Disclaimer Section */}
      <section className="py-16 bg-yellow-50 border-t border-yellow-200">
        <div className="container-max section-padding">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-4xl mx-auto"
          >
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <AlertTriangle className="h-6 w-6 text-yellow-600 mt-1" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-yellow-800 mb-2">
                  Important Medical Disclaimer
                </h3>
                <div className="text-yellow-700 space-y-2 text-sm">
                  <p>
                    The predictions and recommendations provided by Gods Health AI are for informational purposes only 
                    and should not be considered as medical advice, diagnosis, or treatment recommendations.
                  </p>
                  <p>
                    Always consult with qualified healthcare professionals before making any medical decisions. 
                    Our AI predictions are tools to support health awareness but cannot replace professional medical judgment.
                  </p>
                  <p>
                    If you have a medical emergency, please contact your local emergency services immediately.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-primary-600 to-indigo-700">
        <div className="container-max section-padding">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center text-white"
          >
            <h2 className="text-3xl lg:text-4xl font-display font-bold mb-4">
              Ready to Start Your Health Journey?
            </h2>
            <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
              Join thousands of users who are taking control of their health with AI-powered insights.
            </p>
            <div className="flex justify-center">
              <a
                href="/predictors"
                className="inline-flex items-center bg-white text-primary-600 hover:bg-gray-100 font-semibold px-8 py-4 rounded-lg transition-colors duration-200"
              >
                <Zap className="mr-2 h-5 w-5" />
                Try Our Predictors
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default About;