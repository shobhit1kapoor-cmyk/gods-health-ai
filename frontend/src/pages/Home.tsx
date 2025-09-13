import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Heart, Brain, Activity, Shield, Zap, Users, Award, TrendingUp, CheckCircle, Star, Clock } from 'lucide-react';

const Home: React.FC = () => {
  const stats = [
    { label: 'Predictions Made', value: '50K+', icon: TrendingUp },
    { label: 'Accuracy Rate', value: '94%', icon: CheckCircle },
    { label: 'Happy Users', value: '10K+', icon: Users },
    { label: 'Health Conditions', value: '25+', icon: Heart }
  ];

  const features = [
    {
      icon: Heart,
      title: 'Heart Disease Prediction',
      description: 'Advanced cardiovascular risk assessment using multiple health indicators'
    },
    {
      icon: Brain,
      title: 'Mental Health Analysis',
      description: 'Comprehensive mental wellness evaluation and personalized recommendations'
    },
    {
      icon: Activity,
      title: 'Lifestyle Assessment',
      description: 'Holistic health scoring based on daily habits and lifestyle choices'
    },
    {
      icon: Shield,
      title: 'Disease Prevention',
      description: 'Proactive health monitoring to prevent chronic conditions'
    }
  ];

  const predictorCategories = [
    {
      title: 'Cardiovascular Health',
      description: 'Predict heart disease, stroke risk, and cardiovascular conditions',
      icon: Heart,
      count: 8,
      color: 'from-red-500 to-pink-600'
    },
    {
      title: 'Mental Wellness',
      description: 'Assess depression, anxiety, and overall mental health status',
      icon: Brain,
      count: 6,
      color: 'from-purple-500 to-indigo-600'
    },
    {
      title: 'Lifestyle & Fitness',
      description: 'Evaluate fitness levels, nutrition, and lifestyle-related health risks',
      icon: Activity,
      count: 7,
      color: 'from-green-500 to-emerald-600'
    },
    {
      title: 'Specialized Conditions',
      description: 'Predict diabetes, cancer risk, and other specialized health conditions',
      icon: Zap,
      count: 4,
      color: 'from-yellow-500 to-orange-600'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-700" />
        
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-primary-200/30 to-indigo-200/30 rounded-full blur-3xl animate-spin" />
          <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-blue-200/30 to-primary-200/30 rounded-full blur-3xl animate-pulse" />
        </div>
        
        <div className="relative container-max section-padding">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="text-center lg:text-left">
              <h1 className="text-4xl lg:text-6xl font-display font-bold text-gray-900 dark:text-white mb-6">
                AI-Powered{' '}
                <span className="gradient-text inline-block">
                  Health Predictions
                </span>{' '}
                for Better Living
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed max-w-2xl">
                Harness the power of advanced artificial intelligence to predict health risks, 
                assess medical conditions, and receive personalized healthcare insights.
              </p>
              <div className="flex justify-center sm:justify-start">
                <Link to="/predictors" className="btn-primary text-lg px-8 py-4 inline-flex items-center group relative overflow-hidden hover:scale-105 transition-transform">
                  <span className="relative z-10">
                    Explore Predictors
                  </span>
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200 relative z-10" />
                  <div className="absolute inset-0 bg-gradient-to-r from-primary-700 to-indigo-700" />
                </Link>
              </div>
            </div>
            
            <div className="relative">
              {/* Floating Icons */}
              <div className="absolute -top-6 -left-6 z-20 bg-gradient-to-br from-primary-500 to-primary-600 p-3 rounded-full shadow-lg animate-bounce">
                <Heart className="h-6 w-6 text-white" />
              </div>
              
              <div className="absolute -top-4 -right-8 z-20 bg-gradient-to-br from-indigo-500 to-indigo-600 p-3 rounded-full shadow-lg animate-pulse">
                <Brain className="h-6 w-6 text-white" />
              </div>
              
              <div className="absolute -bottom-6 -right-4 z-20 bg-gradient-to-br from-green-500 to-green-600 p-3 rounded-full shadow-lg animate-spin">
                <Activity className="h-6 w-6 text-white" />
              </div>
              
              <div className="relative z-10 bg-white dark:bg-gray-800 rounded-2xl shadow-large p-8 transition-colors duration-300 backdrop-blur-sm bg-opacity-95 dark:bg-opacity-95">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Health Dashboard
                  </h3>
                  <div className="flex space-x-2">
                    <div className="w-3 h-3 bg-red-400 rounded-full animate-pulse"></div>
                    <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
                    <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/20 rounded-lg cursor-pointer hover:scale-105 transition-transform">
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Heart Rate</span>
                    </div>
                    <span className="text-sm font-bold text-green-600 dark:text-green-400 animate-pulse">72 BPM</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg cursor-pointer hover:scale-105 transition-transform">
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Blood Pressure</span>
                    </div>
                    <span className="text-sm font-bold text-blue-600 dark:text-blue-400 animate-pulse">120/80</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg cursor-pointer hover:scale-105 transition-transform">
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Stress Level</span>
                    </div>
                    <span className="text-sm font-bold text-purple-600 dark:text-purple-400 animate-pulse">Low</span>
                  </div>
                </div>
                
                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-4 mt-6">
                  {stats.map((stat, index) => {
                    const Icon = stat.icon;
                    return (
                      <div key={stat.label} className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg cursor-pointer group hover:scale-105 transition-all">
                        <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-2 group-hover:scale-110 transition-transform">
                          <Icon className="h-4 w-4 text-primary-600 animate-pulse" />
                        </div>
                        <div className="text-lg font-bold text-gray-900 dark:text-white hover:scale-110 transition-all animate-pulse">{stat.value}</div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">{stat.label}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="container-max section-padding">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-display font-bold text-gray-900 dark:text-white mb-4">
              Advanced AI Health Predictions
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Our cutting-edge machine learning algorithms analyze multiple health indicators to provide accurate predictions and personalized recommendations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={feature.title} className="group relative p-6 bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-large transition-all duration-300 hover:-translate-y-2">
                  <div className="absolute inset-0 bg-gradient-to-br from-primary-50 to-indigo-50 dark:from-primary-900/20 dark:to-indigo-900/20 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:scale-105"></div>
                  
                  <div className="relative z-10">
                    <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 group-hover:rotate-12 group-hover:scale-110 transition-transform">
                      <div className="animate-bounce">
                        <Icon className="h-6 w-6 text-primary-600" />
                      </div>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Predictor Categories Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container-max section-padding">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-display font-bold text-gray-900 dark:text-white mb-4">
              Comprehensive Health Predictions
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Explore our wide range of AI-powered health predictors, each designed to provide accurate insights into different aspects of your health and wellness.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {predictorCategories.map((category, index) => {
              const Icon = category.icon;
              return (
                <div key={category.title} className="group relative bg-white dark:bg-gray-900 rounded-xl shadow-md hover:shadow-large transition-all duration-300 overflow-hidden hover:-translate-y-2">
                  <div className={`absolute inset-0 bg-gradient-to-br ${category.color} opacity-5 group-hover:opacity-10 transition-opacity duration-300`}></div>
                  
                  <div className="relative p-8">
                    <div className="flex items-start space-x-4">
                      <div className={`w-16 h-16 bg-gradient-to-br ${category.color} rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform`}>
                        <Icon className="h-8 w-8 text-white" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                            {category.title}
                          </h3>
                          <span className="text-sm font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded-full">
                            {category.count} predictors
                          </span>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 mb-4">
                          {category.description}
                        </p>
                        <Link 
                          to="/predictors" 
                          className="inline-flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium group-hover:translate-x-1 transition-transform duration-200"
                        >
                          Explore Predictors
                          <ArrowRight className="ml-1 h-4 w-4" />
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-primary-600 to-indigo-700">
        <div className="container-max section-padding">
          <div className="text-center text-white">
            <h2 className="text-3xl lg:text-4xl font-display font-bold mb-4">
              Ready to Take Control of Your Health?
            </h2>
            <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
              Join thousands of users who trust our AI-powered health predictions to make informed decisions about their wellness journey.
            </p>
            <div className="flex justify-center">
              <Link to="/predictors" className="btn-secondary text-lg px-8 py-4 hover:scale-105 transition-transform">
                Start Predicting
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;