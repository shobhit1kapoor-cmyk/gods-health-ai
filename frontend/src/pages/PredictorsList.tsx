import React, { useState, useEffect, useMemo } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Heart,
  Brain,
  Activity,
  Stethoscope,
  Search,
  Filter,
  TrendingUp,
  Lock,
  Zap,
  Users,
  ChevronRight,
  Clock
} from 'lucide-react';

interface Predictor {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: React.ComponentType<any>;
  difficulty: 'Easy' | 'Medium' | 'Advanced';
  estimatedTime: string;
  accuracy: string;
  featured?: boolean;
  status?: 'ready' | 'working';
}

const PredictorsList: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'all');
  const [filteredPredictors, setFilteredPredictors] = useState<Predictor[]>([]);

  const predictors: Predictor[] = useMemo(() => [
    // TOP 5 PREDICTORS - Ready for Use
    {
      id: 'sepsis',
      name: 'Sepsis Predictor',
      description: 'Early sepsis detection in hospital settings - a life-saving diagnostic tool.',
      category: 'condition-complications',
      icon: Zap,
      difficulty: 'Advanced',
      estimatedTime: '3-5 min',
      accuracy: '96%',
      featured: true,
      status: 'ready'
    },
    {
      id: 'heart_disease',
      name: 'Heart Disease Predictor',
      description: 'Predict risk of heart attack, arrhythmia, or heart failure using cardiovascular health indicators.',
      category: 'disease-risk-diagnosis',
      icon: Heart,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '94%',
      featured: true,
      status: 'ready'
    },
    {
      id: 'stroke_risk',
      name: 'Stroke Risk Predictor',
      description: 'Analyze blood pressure, cholesterol, lifestyle, and family history to assess stroke risk.',
      category: 'disease-risk-diagnosis',
      icon: Brain,
      difficulty: 'Medium',
      estimatedTime: '6-8 min',
      accuracy: '92%',
      featured: true,
      status: 'ready'
    },
    {
      id: 'anemia',
      name: 'Anemia Predictor',
      description: 'Detect various types of anemia using comprehensive blood test analysis.',
      category: 'specialized',
      icon: Stethoscope,
      difficulty: 'Easy',
      estimatedTime: '3-5 min',
      accuracy: '92%',
      featured: true,
      status: 'ready'
    },
    {
      id: 'diabetes',
      name: 'Diabetes Risk Predictor',
      description: 'Predict Type 2 diabetes risk using glucose levels, BMI, family history, and lifestyle factors.',
      category: 'disease-risk-diagnosis',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '87%',
      featured: true,
      status: 'ready'
    },

    // OTHER PREDICTORS - Still Working On
    {
      id: 'cancer_detection',
      name: 'Cancer Detection & Risk',
      description: 'Comprehensive cancer risk assessment for breast, lung, prostate, skin, and cervical cancers.',
      category: 'disease-risk-diagnosis',
      icon: Lock,
      difficulty: 'Advanced',
      estimatedTime: '10-12 min',
      accuracy: '89%',
      status: 'working'
    },
    {
      id: 'kidney_disease',
      name: 'Kidney Disease Predictor',
      description: 'Chronic kidney disease detection using blood and urine test data.',
      category: 'disease-risk-diagnosis',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '4-6 min',
      accuracy: '91%',
      status: 'working'
    },
    {
      id: 'liver_disease',
      name: 'Liver Disease Predictor',
      description: 'Detect hepatitis, cirrhosis, and fatty liver disease from laboratory test results.',
      category: 'disease-risk-diagnosis',
      icon: Stethoscope,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '88%',
      status: 'working'
    },
    {
      id: 'alzheimer',
      name: 'Alzheimer\'s Predictor',
      description: 'Early detection of Alzheimer\'s and dementia using memory and behavioral assessment data.',
      category: 'disease-risk-diagnosis',
      icon: Brain,
      difficulty: 'Advanced',
      estimatedTime: '8-10 min',
      accuracy: '85%',
      status: 'working'
    },
    {
      id: 'parkinson',
      name: 'Parkinson\'s Disease Predictor',
      description: 'Analyze voice patterns, tremor, and movement data for Parkinson\'s disease detection.',
      category: 'disease-risk-diagnosis',
      icon: Activity,
      difficulty: 'Advanced',
      estimatedTime: '7-9 min',
      accuracy: '87%',
      status: 'working'
    },
    {
      id: 'hospital_readmission',
      name: 'Hospital Readmission Predictor',
      description: 'Predict likelihood of patient readmission within 30 days of discharge.',
      category: 'condition-complications',
      icon: Users,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '83%',
      status: 'working'
    },
    {
      id: 'icu_mortality',
      name: 'ICU Mortality Predictor',
      description: 'Survival prediction based on vital signs and laboratory results in ICU settings.',
      category: 'condition-complications',
      icon: Activity,
      difficulty: 'Advanced',
      estimatedTime: '4-6 min',
      accuracy: '91%',
      status: 'working'
    },
    {
      id: 'post_surgery_complication',
      name: 'Post-Surgery Complication Predictor',
      description: 'Assess risks and predict complications following major surgical procedures.',
      category: 'condition-complications',
      icon: Stethoscope,
      difficulty: 'Advanced',
      estimatedTime: '6-8 min',
      accuracy: '86%',
      status: 'working'
    },
    {
      id: 'pregnancy_complication',
      name: 'Pregnancy Complication Predictor',
      description: 'Predict gestational diabetes, preeclampsia, and other pregnancy-related complications.',
      category: 'condition-complications',
      icon: Heart,
      difficulty: 'Medium',
      estimatedTime: '7-9 min',
      accuracy: '89%',
      status: 'working'
    },

    // Lifestyle & Preventive Health Predictors
    {
      id: 'obesity_risk',
      name: 'Obesity & BMI Risk Predictor',
      description: 'Assess long-term obesity complications and metabolic health risks.',
      category: 'lifestyle-prevention',
      icon: TrendingUp,
      difficulty: 'Easy',
      estimatedTime: '3-5 min',
      accuracy: '87%',
      status: 'working'
    },
    {
      id: 'hypertension',
      name: 'Hypertension Predictor',
      description: 'Evaluate lifestyle and genetic risk factors for high blood pressure development.',
      category: 'lifestyle-prevention',
      icon: Activity,
      difficulty: 'Easy',
      estimatedTime: '4-6 min',
      accuracy: '90%',
      status: 'working'
    },
    {
      id: 'cholesterol_risk',
      name: 'Cholesterol Risk Predictor',
      description: 'Assess atherosclerosis risk and plaque buildup leading to stroke or heart attack.',
      category: 'lifestyle-prevention',
      icon: Heart,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '88%',
      status: 'working'
    },
    {
      id: 'mental_health',
      name: 'Mental Health Predictor',
      description: 'Depression and anxiety detection using surveys, voice analysis, and wearable data.',
      category: 'lifestyle-prevention',
      icon: Brain,
      difficulty: 'Medium',
      estimatedTime: '8-10 min',
      accuracy: '84%',
      status: 'working'
    },
    {
      id: 'sleep_apnea',
      name: 'Sleep Apnea Predictor',
      description: 'Detect sleep disorders using wearable device data and questionnaire responses.',
      category: 'lifestyle-prevention',
      icon: Activity,
      difficulty: 'Easy',
      estimatedTime: '6-8 min',
      accuracy: '86%',
      status: 'working'
    },

    // Specialized Predictors
    {
      id: 'covid_risk',
      name: 'COVID-19 Risk Predictor',
      description: 'Assess COVID-19 severity and hospitalization risk based on health profile.',
      category: 'specialized',
      icon: Lock,
      difficulty: 'Medium',
      estimatedTime: '4-6 min',
      accuracy: '89%',
      status: 'working'
    },
    {
      id: 'asthma_copd',
      name: 'Asthma & COPD Predictor',
      description: 'Predict respiratory disease progression and exacerbation risks.',
      category: 'specialized',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '87%',
      status: 'working'
    },
    {
      id: 'thyroid_disorder',
      name: 'Thyroid Disorder Predictor',
      description: 'Detect hyperthyroidism and hypothyroidism using thyroid function tests.',
      category: 'specialized',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '4-6 min',
      accuracy: '90%',
      status: 'working'
    },
    {
      id: 'cancer_recurrence',
      name: 'Cancer Recurrence Predictor',
      description: 'Predict likelihood of cancer recurrence after successful treatment.',
      category: 'specialized',
      icon: Lock,
      difficulty: 'Advanced',
      estimatedTime: '8-10 min',
      accuracy: '85%',
      status: 'working'
    }
  ], []);

  const categories = [
    { id: 'all', name: 'All Predictors', count: predictors.length },
    { id: 'disease-risk-diagnosis', name: 'Disease Risk & Diagnosis', count: predictors.filter(p => p.category === 'disease-risk-diagnosis').length },
    { id: 'condition-complications', name: 'Condition & Complications', count: predictors.filter(p => p.category === 'condition-complications').length },
    { id: 'lifestyle-prevention', name: 'Lifestyle & Prevention', count: predictors.filter(p => p.category === 'lifestyle-prevention').length },
    { id: 'specialized', name: 'Specialized Care', count: predictors.filter(p => p.category === 'specialized').length }
  ];

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300';
      case 'Medium': return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300';
      case 'Advanced': return 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300';
    }
  };

  useEffect(() => {
    let filtered = predictors;

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(predictor => predictor.category === selectedCategory);
    }

    if (searchTerm) {
      filtered = filtered.filter(predictor =>
        predictor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        predictor.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredPredictors(filtered);
  }, [searchTerm, selectedCategory, predictors]);



  return (
    <div className="min-h-screen py-8">
      <div className="container-max section-padding">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl lg:text-5xl font-display font-bold text-gray-900 dark:text-white mb-4">
            Health AI Predictors
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Explore our comprehensive collection of AI-powered health predictors. 
            Get instant risk assessments and personalized recommendations.
          </p>
        </motion.div>



        {/* Search and Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mb-8"
        >
          <div className="flex flex-col lg:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search predictors..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10 w-full"
              />
            </div>
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="input pl-10 pr-8 appearance-none bg-white dark:bg-gray-800 min-w-[200px]"
              >
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name} ({category.count})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </motion.div>

        {/* Predictors Grid */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          {filteredPredictors.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <Search className="h-16 w-16 mx-auto" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No predictors found</h3>
              <p className="text-gray-600 dark:text-gray-300">Try adjusting your search terms or filters.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPredictors.map((predictor, index) => {
                const Icon = predictor.icon;
                return (
                  <motion.div
                    key={predictor.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.05 }}
                  >
                    <div className={`block card transition-all duration-300 group h-full hover:shadow-large cursor-pointer ${
                      predictor.status === 'working' ? 'opacity-90' : ''
                    }`}>
                      <Link to={`/predictor/${predictor.id}`} className="block h-full">
                          <div className="flex items-start space-x-4 mb-4">
                            <div className={`w-12 h-12 rounded-lg flex items-center justify-center group-hover:bg-primary-200 dark:group-hover:bg-primary-800/50 transition-colors duration-300 ${
                              predictor.status === 'working' 
                                ? 'bg-yellow-100 dark:bg-yellow-900/30' 
                                : 'bg-primary-100 dark:bg-primary-900/30'
                            }`}>
                              <Icon className={`h-6 w-6 ${
                                predictor.status === 'working'
                                  ? 'text-yellow-600 dark:text-yellow-400'
                                  : 'text-primary-600 dark:text-primary-400'
                              }`} />
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200">
                                  {predictor.name}
                                </h3>
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                  predictor.status === 'working'
                                    ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300'
                                    : 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
                                }`}>
                                  {predictor.status === 'working' ? 'Still Working On' : 'Ready'}
                                </span>
                              </div>
                              <p className="text-gray-600 dark:text-gray-300 text-sm line-clamp-3">
                                {predictor.description}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center justify-between text-sm mt-auto">
                            <div className="flex items-center space-x-4">
                              <div className="flex items-center text-gray-500 dark:text-gray-400">
                                <Clock className="h-4 w-4 mr-1" />
                                {predictor.estimatedTime}
                              </div>
                              <div className={`font-medium ${
                                predictor.status === 'working'
                                  ? 'text-yellow-600 dark:text-yellow-400'
                                  : 'text-green-600 dark:text-green-400'
                              }`}>
                                {predictor.accuracy}
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(predictor.difficulty)}`}>
                                {predictor.difficulty}
                              </span>
                              <ChevronRight className="h-4 w-4 text-gray-400 dark:text-gray-500 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200" />
                            </div>
                          </div>

                      </Link>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default PredictorsList;