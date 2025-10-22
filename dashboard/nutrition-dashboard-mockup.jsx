import React, { useState } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { TrendingUp, Users, MapPin, Activity, AlertCircle, CheckCircle, Info } from 'lucide-react';

// Main App Component with Navigation
const ChildNutritionDashboard = () => {
  const [currentPage, setCurrentPage] = useState('overview');
  const [loadingAI, setLoadingAI] = useState({});

  // Navigation component
  const Sidebar = () => {
    const menuItems = [
      { id: 'overview', label: 'Overview', icon: <Activity /> },
      { id: 'location', label: 'Location Analysis', icon: <MapPin /> },
      { id: 'child', label: 'Child Analysis', icon: <Users /> }
    ];

    return (
      <div style={{
        width: '250px',
        background: 'linear-gradient(180deg, #2D3748 0%, #1A202C 100%)',
        color: 'white',
        padding: '24px 0',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        boxShadow: '4px 0 12px rgba(0,0,0,0.1)'
      }}>
        <div style={{ padding: '0 24px', marginBottom: '40px' }}>
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', margin: 0, marginBottom: '8px' }}>
            Child Nutrition
          </h2>
          <p style={{ fontSize: '14px', color: '#A0AEC0', margin: 0 }}>Impact Dashboard</p>
        </div>
        
        {menuItems.map(item => (
          <div
            key={item.id}
            onClick={() => setCurrentPage(item.id)}
            style={{
              padding: '16px 24px',
              cursor: 'pointer',
              background: currentPage === item.id ? 'rgba(66, 153, 225, 0.2)' : 'transparent',
              borderLeft: currentPage === item.id ? '4px solid #4299E1' : '4px solid transparent',
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              transition: 'all 0.2s',
              ':hover': {
                background: 'rgba(66, 153, 225, 0.1)'
              }
            }}
            onMouseEnter={(e) => {
              if (currentPage !== item.id) {
                e.currentTarget.style.background = 'rgba(66, 153, 225, 0.1)';
              }
            }}
            onMouseLeave={(e) => {
              if (currentPage !== item.id) {
                e.currentTarget.style.background = 'transparent';
              }
            }}
          >
            <span style={{ fontSize: '20px' }}>{item.icon}</span>
            <span style={{ fontSize: '16px', fontWeight: currentPage === item.id ? '600' : '400' }}>
              {item.label}
            </span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', background: '#F7FAFC', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{ marginLeft: '250px', flex: 1, padding: '32px' }}>
        {currentPage === 'overview' && <OverviewPage loadingAI={loadingAI} setLoadingAI={setLoadingAI} />}
        {currentPage === 'location' && <LocationPage />}
        {currentPage === 'child' && <ChildPage />}
      </div>
    </div>
  );
};

// AI Interpretation Component
const AIInterpretation = ({ graphId, graphTitle, loadingAI, setLoadingAI }) => {
  const [interpretation, setInterpretation] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const getAIInterpretation = async () => {
    setLoadingAI(prev => ({ ...prev, [graphId]: true }));
    setIsExpanded(true);

    // Simulated AI interpretation based on graph type
    const interpretations = {
      'stunting-overview': "The data shows significant positive progress in child nutrition outcomes. Between first and last measurements, we observe a 28% reduction in stunting rates (from 21% to 15%) and a 38% reduction in severe stunting (from 8% to 5%). The 'at risk' category decreased from 12% to 11%, demonstrating effective intervention. This suggests that the nutrition programs are having a measurable impact on child growth and development. The target of 2.5% stunting and 0.15% severe stunting represents ambitious goals that would align with WHO recommendations for healthy child populations.",
      
      'children-measured': "The measurement data reveals strong program engagement with 5,725 total children measured across both time periods. The distribution shows 665 children at risk of stunting at first measurement, decreasing to 625 at last measurement. Most notably, the stunted population decreased from 1,205 to 836 children (-31%), while severely stunted children dropped from 477 to 288 (-40%). These trends indicate successful interventions, particularly for children in the most critical categories. The data suggests consistent monitoring practices with most children receiving multiple measurements over time.",
      
      'temporal-trends': "The 4.5-year longitudinal data (November 2020 - May 2025) shows consistent program delivery across 36,050 measurement records. Peak collection occurred during 2021-2022, suggesting program scale-up during this period. The temporal distribution indicates sustained engagement with beneficiaries, with an average of 3.95 measurements per child. This frequent monitoring enables early detection of growth faltering and timely interventions.",
      
      'geographic-reach': "Geographic analysis reveals strong program concentration in key areas: Sasolburg (27.8%), Wentworth ECD Forum Durban (16.8%), and Kuyasa (14.8%) account for nearly 60% of all measurements. The program successfully operates across 29 distinct sites with 201 household units/ECD centers. Safripol site group represents 55.6% of total reach, while Jannie Mouton covers 35.8%, indicating strategic partnerships with major stakeholders. The geographic diversity ensures broad impact across different communities in South Africa.",
      
      'who-zscore': "The WHO height-for-age z-score analysis shows a mean of -0.64, indicating the population is slightly below the WHO median for expected height. While this is above the stunting threshold (-2), it suggests room for improvement. The distribution ranges from -4 to +4, with most children clustered around the mean. The negative deviation indicates historical or ongoing nutritional challenges, but the improvement from first to last measurement demonstrates that interventions are moving children toward healthier growth trajectories.",
      
      'program-quality': "Data quality metrics are strong with a mean quality score of 3.17/4.0 (79%), indicating reliable measurements. Only 7% of records are flagged for review, suggesting robust data collection protocols. The 100% completion rate for critical fields (BeneficiaryId, Answer, Capture Date, Site) demonstrates excellent data governance. The removal of 30.2% duplicates during cleaning improved dataset integrity. High measurement consistency across sites enables reliable program evaluation and impact assessment."
    };

    // Simulate API call delay
    setTimeout(() => {
      setInterpretation(interpretations[graphId] || "This visualization shows important trends in child nutrition outcomes. The data suggests positive program impact with measurable improvements in stunting indicators over time.");
      setLoadingAI(prev => ({ ...prev, [graphId]: false }));
    }, 1500);
  };

  return (
    <div style={{
      marginTop: '16px',
      border: '1px solid #E2E8F0',
      borderRadius: '8px',
      overflow: 'hidden'
    }}>
      <button
        onClick={getAIInterpretation}
        disabled={loadingAI[graphId]}
        style={{
          width: '100%',
          padding: '12px 16px',
          background: isExpanded ? '#EBF8FF' : 'white',
          border: 'none',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          cursor: loadingAI[graphId] ? 'wait' : 'pointer',
          fontSize: '14px',
          fontWeight: '500',
          color: '#2B6CB0',
          transition: 'all 0.2s'
        }}
        onMouseEnter={(e) => {
          if (!loadingAI[graphId]) {
            e.currentTarget.style.background = '#EBF8FF';
          }
        }}
        onMouseLeave={(e) => {
          if (!isExpanded) {
            e.currentTarget.style.background = 'white';
          }
        }}
      >
        <Info size={16} />
        {loadingAI[graphId] ? 'Generating AI Interpretation...' : 
         interpretation ? 'AI Interpretation' : 'Get AI Interpretation'}
      </button>
      
      {interpretation && (
        <div style={{
          padding: '16px',
          background: '#F7FAFC',
          borderTop: '1px solid #E2E8F0',
          fontSize: '14px',
          lineHeight: '1.6',
          color: '#2D3748'
        }}>
          <div style={{
            display: 'flex',
            gap: '12px',
            alignItems: 'flex-start'
          }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
              marginTop: '2px'
            }}>
              <span style={{ color: 'white', fontSize: '16px' }}>🤖</span>
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: '600', marginBottom: '8px', color: '#2B6CB0' }}>
                AI Analysis: {graphTitle}
              </div>
              {interpretation}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Overview Page Component
const OverviewPage = ({ loadingAI, setLoadingAI }) => {
  const COLORS = {
    atRisk: '#F6AD55',    // Orange
    stunted: '#FC8181',   // Red/Coral
    severelyStunted: '#E53E3E', // Dark Red
    normal: '#68D391',    // Green
    primary: '#4299E1',   // Blue
    secondary: '#9F7AEA'  // Purple
  };

  // Dummy data for stunting progression
  const stuntingProgressionData = [
    { category: 'First Measurement', atRisk: 12, stunted: 21, severelyStunted: 8 },
    { category: 'Last Measurement', atRisk: 11, stunted: 15, severelyStunted: 5 },
    { category: 'Target Goal', atRisk: 2.5, stunted: 2.5, severelyStunted: 0.15 }
  ];

  // Children measured data
  const childrenMeasuredData = [
    { measurement: 'First', atRisk: 665, stunted: 1205, severelyStunted: 477 },
    { measurement: 'Last', atRisk: 625, stunted: 836, severelyStunted: 288 },
    { measurement: 'Target', atRisk: 143, stunted: 143, severelyStunted: 9 }
  ];

  // Temporal trends
  const temporalTrendsData = [
    { period: 'Nov 2020', measurements: 450, avgZScore: -0.82, stunted: 28 },
    { period: 'Q1 2021', measurements: 1250, avgZScore: -0.78, stunted: 26 },
    { period: 'Q2 2021', measurements: 2100, avgZScore: -0.74, stunted: 24 },
    { period: 'Q3 2021', measurements: 2800, avgZScore: -0.71, stunted: 22 },
    { period: 'Q4 2021', measurements: 3200, avgZScore: -0.69, stunted: 21 },
    { period: 'Q1 2022', measurements: 3450, avgZScore: -0.68, stunted: 20 },
    { period: 'Q2 2022', measurements: 3600, avgZScore: -0.67, stunted: 19 },
    { period: 'Q3 2022', measurements: 3100, avgZScore: -0.66, stunted: 18 },
    { period: 'Q4 2022', measurements: 2900, avgZScore: -0.65, stunted: 17 },
    { period: 'Q1 2023', measurements: 2800, avgZScore: -0.65, stunted: 16 },
    { period: 'Q2 2023', measurements: 2650, avgZScore: -0.64, stunted: 16 },
    { period: 'Q3 2023', measurements: 2500, avgZScore: -0.64, stunted: 15 },
    { period: 'Q4 2023', measurements: 2400, avgZScore: -0.63, stunted: 15 },
    { period: 'Q1 2024', measurements: 2100, avgZScore: -0.63, stunted: 15 },
    { period: 'Q2 2024', measurements: 1800, avgZScore: -0.64, stunted: 15 },
    { period: 'Q3 2024', measurements: 1200, avgZScore: -0.64, stunted: 15 },
    { period: 'May 2025', measurements: 350, avgZScore: -0.64, stunted: 15 }
  ];

  // Geographic reach data
  const geographicData = [
    { name: 'Sasolburg', children: 10009, percentage: 27.8, avgZScore: -0.62 },
    { name: 'Wentworth ECD', children: 6062, percentage: 16.8, avgZScore: -0.68 },
    { name: 'Kuyasa', children: 5319, percentage: 14.8, avgZScore: -0.59 },
    { name: 'NG KERK Hoopstad', children: 3689, percentage: 10.2, avgZScore: -0.71 },
    { name: 'Miqlat Paarl', children: 2034, percentage: 5.6, avgZScore: -0.55 },
    { name: 'Stellumthombo', children: 2005, percentage: 5.6, avgZScore: -0.58 },
    { name: 'Other Sites', children: 6932, percentage: 19.2, avgZScore: -0.66 }
  ];

  // Site group distribution
  const siteGroupData = [
    { name: 'Safripol', value: 55.6, children: 20063 },
    { name: 'Jannie Mouton', value: 35.8, children: 12912 },
    { name: 'GROOT Swem', value: 3.5, children: 1268 },
    { name: 'Villa Crop', value: 2.5, children: 885 },
    { name: 'Others', value: 2.6, children: 922 }
  ];

  // Key metrics cards
  const MetricCard = ({ title, value, subtitle, icon, trend, color }) => (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      padding: '24px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      border: '1px solid #E2E8F0'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{
          width: '48px',
          height: '48px',
          borderRadius: '12px',
          background: `${color}20`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: color
        }}>
          {icon}
        </div>
        {trend && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            color: trend > 0 ? '#48BB78' : '#F56565',
            fontSize: '14px',
            fontWeight: '600'
          }}>
            <TrendingUp size={16} style={{ transform: trend < 0 ? 'rotate(180deg)' : 'none' }} />
            {Math.abs(trend)}%
          </div>
        )}
      </div>
      <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#2D3748', marginBottom: '4px' }}>
        {value}
      </div>
      <div style={{ fontSize: '14px', color: '#718096', marginBottom: '8px' }}>
        {title}
      </div>
      {subtitle && (
        <div style={{ fontSize: '12px', color: '#A0AEC0' }}>
          {subtitle}
        </div>
      )}
    </div>
  );

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#2D3748', margin: 0, marginBottom: '8px' }}>
          Program Overview
        </h1>
        <p style={{ fontSize: '16px', color: '#718096', margin: 0 }}>
          Comprehensive child nutrition impact analysis • Last updated: October 2024
        </p>
      </div>

      {/* Key Metrics */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '20px',
        marginBottom: '32px'
      }}>
        <MetricCard
          title="Total Children Measured"
          value="36,050"
          subtitle="Across 5,725 unique children"
          icon={<Users size={24} />}
          color={COLORS.primary}
        />
        <MetricCard
          title="Active Sites"
          value="29"
          subtitle="Across South Africa"
          icon={<MapPin size={24} />}
          color={COLORS.secondary}
        />
        <MetricCard
          title="Stunting Reduction"
          value="28%"
          subtitle="First to last measurement"
          icon={<TrendingUp size={24} />}
          trend={-28}
          color="#48BB78"
        />
        <MetricCard
          title="Avg WHO Z-Score"
          value="-0.64"
          subtitle="Improving toward 0 target"
          icon={<Activity size={24} />}
          color={COLORS.atRisk}
        />
      </div>

      {/* Stunting Progression Chart */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Stunting Category Progress (Percentage of Children)
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={stuntingProgressionData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="category" stroke="#718096" />
            <YAxis stroke="#718096" label={{ value: 'Percentage (%)', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
              formatter={(value) => `${value}%`}
            />
            <Legend />
            <Bar dataKey="atRisk" name="At Risk of Stunting" fill={COLORS.atRisk} radius={[8, 8, 0, 0]} />
            <Bar dataKey="stunted" name="Stunted" fill={COLORS.stunted} radius={[8, 8, 0, 0]} />
            <Bar dataKey="severelyStunted" name="Severely Stunted" fill={COLORS.severelyStunted} radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId="stunting-overview" 
          graphTitle="Stunting Category Progress"
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

      {/* Children Measured Absolute Numbers */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Number of Children by Stunting Category
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={childrenMeasuredData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="measurement" stroke="#718096" />
            <YAxis stroke="#718096" label={{ value: 'Number of Children', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
            />
            <Legend />
            <Bar dataKey="atRisk" name="At Risk" fill={COLORS.atRisk} radius={[8, 8, 0, 0]} />
            <Bar dataKey="stunted" name="Stunted" fill={COLORS.stunted} radius={[8, 8, 0, 0]} />
            <Bar dataKey="severelyStunted" name="Severely Stunted" fill={COLORS.severelyStunted} radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId="children-measured" 
          graphTitle="Children Measured by Category"
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

      {/* Temporal Trends */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Temporal Trends: Measurements & Stunting Rates
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart data={temporalTrendsData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="period" stroke="#718096" angle={-45} textAnchor="end" height={80} />
            <YAxis yAxisId="left" stroke="#718096" label={{ value: 'Measurements', angle: -90, position: 'insideLeft' }} />
            <YAxis yAxisId="right" orientation="right" stroke="#718096" label={{ value: 'Stunting %', angle: 90, position: 'insideRight' }} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
            />
            <Legend />
            <Area yAxisId="left" type="monotone" dataKey="measurements" name="Measurements" stroke={COLORS.primary} fill={COLORS.primary} fillOpacity={0.3} />
            <Line yAxisId="right" type="monotone" dataKey="stunted" name="Stunting %" stroke={COLORS.severelyStunted} strokeWidth={3} dot={{ r: 4 }} />
          </AreaChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId="temporal-trends" 
          graphTitle="Temporal Trends"
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

      {/* Geographic and Program Distribution */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '24px' }}>
        {/* Top Sites */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '24px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          border: '1px solid #E2E8F0'
        }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
            Top Sites by Children Measured
          </h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={geographicData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
              <XAxis type="number" stroke="#718096" />
              <YAxis dataKey="name" type="category" stroke="#718096" width={120} />
              <Tooltip 
                contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
              />
              <Bar dataKey="children" fill={COLORS.primary} radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <AIInterpretation 
            graphId="geographic-reach" 
            graphTitle="Geographic Reach"
            loadingAI={loadingAI}
            setLoadingAI={setLoadingAI}
          />
        </div>

        {/* Program Partners */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '24px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          border: '1px solid #E2E8F0'
        }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
            Program Distribution by Site Group
          </h3>
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={siteGroupData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
              >
                {siteGroupData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={[COLORS.primary, COLORS.secondary, COLORS.atRisk, '#48BB78', '#9F7AEA'][index % 5]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
                formatter={(value, name, props) => [`${value}% (${props.payload.children} children)`, name]}
              />
            </PieChart>
          </ResponsiveContainer>
          <AIInterpretation 
            graphId="program-quality" 
            graphTitle="Program Distribution"
            loadingAI={loadingAI}
            setLoadingAI={setLoadingAI}
          />
        </div>
      </div>

      {/* WHO Z-Score Distribution */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          WHO Height-for-Age Z-Score Analysis
        </h3>
        <div style={{ marginBottom: '16px', padding: '12px', background: '#EBF8FF', borderRadius: '8px', fontSize: '14px' }}>
          <strong>Current Mean Z-Score: -0.64</strong> • WHO Normal Range: -2 to +2 • Target: 0 (WHO median)
        </div>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={[
            { zScore: -4, frequency: 12 },
            { zScore: -3, frequency: 145 },
            { zScore: -2, frequency: 1288 },
            { zScore: -1, frequency: 5420 },
            { zScore: -0.64, frequency: 8200 },
            { zScore: 0, frequency: 7100 },
            { zScore: 1, frequency: 4800 },
            { zScore: 2, frequency: 2100 },
            { zScore: 3, frequency: 320 },
            { zScore: 4, frequency: 28 }
          ]}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="zScore" stroke="#718096" label={{ value: 'Z-Score', position: 'insideBottom', offset: -5 }} />
            <YAxis stroke="#718096" label={{ value: 'Number of Children', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
            />
            <Line type="monotone" dataKey="frequency" stroke={COLORS.primary} strokeWidth={3} dot={{ r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId="who-zscore" 
          graphTitle="WHO Z-Score Distribution"
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

    </div>
  );
};

// Location Analysis Page
const LocationPage = () => {
  const [selectedLocation, setSelectedLocation] = useState('Sasolburg');
  const [loadingAI, setLoadingAI] = useState({});

  const COLORS = {
    atRisk: '#F6AD55',
    stunted: '#FC8181',
    severelyStunted: '#E53E3E',
    normal: '#68D391',
    primary: '#4299E1',
    secondary: '#9F7AEA'
  };

  // All available locations with their data
  const locationsData = {
    'Sasolburg': {
      siteGroup: 'Safripol',
      totalChildren: 10009,
      totalMeasurements: 10009,
      avgZScore: -0.62,
      stuntingRate: 14.2,
      severeStuntingRate: 4.8,
      atRiskRate: 11.5,
      households: 45,
      temporalData: [
        { period: 'Q4 2020', measurements: 420, avgZScore: -0.78, stunting: 18.5, severeStunting: 7.2 },
        { period: 'Q1 2021', measurements: 850, avgZScore: -0.74, stunting: 17.8, severeStunting: 6.8 },
        { period: 'Q2 2021', measurements: 1200, avgZScore: -0.71, stunting: 16.5, severeStunting: 6.1 },
        { period: 'Q3 2021', measurements: 1450, avgZScore: -0.68, stunting: 15.8, severeStunting: 5.6 },
        { period: 'Q4 2021', measurements: 1380, avgZScore: -0.66, stunting: 15.2, severeStunting: 5.2 },
        { period: 'Q1 2022', measurements: 1250, avgZScore: -0.64, stunting: 14.8, severeStunting: 5.0 },
        { period: 'Q2 2022', measurements: 1180, avgZScore: -0.63, stunting: 14.5, severeStunting: 4.9 },
        { period: 'Q3 2022', measurements: 980, avgZScore: -0.62, stunting: 14.3, severeStunting: 4.8 },
        { period: 'Q4 2022', measurements: 820, avgZScore: -0.62, stunting: 14.2, severeStunting: 4.8 },
        { period: 'Q1 2023', measurements: 479, avgZScore: -0.62, stunting: 14.2, severeStunting: 4.8 }
      ],
      categoryBreakdown: [
        { category: 'Normal', count: 6956, percentage: 69.5 },
        { category: 'At Risk', count: 1151, percentage: 11.5 },
        { category: 'Stunted', count: 1422, percentage: 14.2 },
        { category: 'Severely Stunted', count: 480, percentage: 4.8 }
      ]
    },
    'Wentworth ECD Forum Durban': {
      siteGroup: 'Jannie Mouton',
      totalChildren: 6062,
      totalMeasurements: 6062,
      avgZScore: -0.68,
      stuntingRate: 16.8,
      severeStuntingRate: 5.4,
      atRiskRate: 12.3,
      households: 28,
      temporalData: [
        { period: 'Q4 2020', measurements: 280, avgZScore: -0.85, stunting: 22.1, severeStunting: 8.9 },
        { period: 'Q1 2021', measurements: 520, avgZScore: -0.80, stunting: 20.5, severeStunting: 7.8 },
        { period: 'Q2 2021', measurements: 780, avgZScore: -0.76, stunting: 19.2, severeStunting: 7.1 },
        { period: 'Q3 2021', measurements: 950, avgZScore: -0.73, stunting: 18.4, severeStunting: 6.5 },
        { period: 'Q4 2021', measurements: 890, avgZScore: -0.71, stunting: 17.9, severeStunting: 6.0 },
        { period: 'Q1 2022', measurements: 820, avgZScore: -0.70, stunting: 17.5, severeStunting: 5.8 },
        { period: 'Q2 2022', measurements: 750, avgZScore: -0.69, stunting: 17.2, severeStunting: 5.6 },
        { period: 'Q3 2022', measurements: 620, avgZScore: -0.68, stunting: 17.0, severeStunting: 5.5 },
        { period: 'Q4 2022', measurements: 452, avgZScore: -0.68, stunting: 16.8, severeStunting: 5.4 }
      ],
      categoryBreakdown: [
        { category: 'Normal', count: 3975, percentage: 65.6 },
        { category: 'At Risk', count: 746, percentage: 12.3 },
        { category: 'Stunted', count: 1018, percentage: 16.8 },
        { category: 'Severely Stunted', count: 327, percentage: 5.4 }
      ]
    },
    'Kuyasa': {
      siteGroup: 'Safripol',
      totalChildren: 5319,
      totalMeasurements: 5319,
      avgZScore: -0.59,
      stuntingRate: 13.1,
      severeStuntingRate: 4.2,
      atRiskRate: 10.8,
      households: 22,
      temporalData: [
        { period: 'Q4 2020', measurements: 350, avgZScore: -0.72, stunting: 16.8, severeStunting: 6.5 },
        { period: 'Q1 2021', measurements: 580, avgZScore: -0.68, stunting: 15.9, severeStunting: 5.9 },
        { period: 'Q2 2021', measurements: 720, avgZScore: -0.65, stunting: 15.2, severeStunting: 5.4 },
        { period: 'Q3 2021', measurements: 850, avgZScore: -0.62, stunting: 14.5, severeStunting: 5.0 },
        { period: 'Q4 2021', measurements: 780, avgZScore: -0.61, stunting: 14.0, severeStunting: 4.7 },
        { period: 'Q1 2022', measurements: 720, avgZScore: -0.60, stunting: 13.6, severeStunting: 4.5 },
        { period: 'Q2 2022', measurements: 650, avgZScore: -0.59, stunting: 13.3, severeStunting: 4.3 },
        { period: 'Q3 2022', measurements: 669, avgZScore: -0.59, stunting: 13.1, severeStunting: 4.2 }
      ],
      categoryBreakdown: [
        { category: 'Normal', count: 3826, percentage: 71.9 },
        { category: 'At Risk', count: 574, percentage: 10.8 },
        { category: 'Stunted', count: 697, percentage: 13.1 },
        { category: 'Severely Stunted', count: 223, percentage: 4.2 }
      ]
    },
    'NG KERK Hoopstad': {
      siteGroup: 'Safripol',
      totalChildren: 3689,
      totalMeasurements: 3689,
      avgZScore: -0.71,
      stuntingRate: 17.5,
      severeStuntingRate: 5.9,
      atRiskRate: 12.8,
      households: 18,
      temporalData: [
        { period: 'Q1 2021', measurements: 420, avgZScore: -0.82, stunting: 21.2, severeStunting: 8.1 },
        { period: 'Q2 2021', measurements: 580, avgZScore: -0.78, stunting: 20.1, severeStunting: 7.4 },
        { period: 'Q3 2021', measurements: 680, avgZScore: -0.75, stunting: 19.3, severeStunting: 6.9 },
        { period: 'Q4 2021', measurements: 620, avgZScore: -0.73, stunting: 18.6, severeStunting: 6.5 },
        { period: 'Q1 2022', measurements: 550, avgZScore: -0.72, stunting: 18.1, severeStunting: 6.2 },
        { period: 'Q2 2022', measurements: 520, avgZScore: -0.71, stunting: 17.8, severeStunting: 6.0 },
        { period: 'Q3 2022', measurements: 319, avgZScore: -0.71, stunting: 17.5, severeStunting: 5.9 }
      ],
      categoryBreakdown: [
        { category: 'Normal', count: 2497, percentage: 67.7 },
        { category: 'At Risk', count: 472, percentage: 12.8 },
        { category: 'Stunted', count: 646, percentage: 17.5 },
        { category: 'Severely Stunted', count: 218, percentage: 5.9 }
      ]
    },
    'Miqlat Paarl': {
      siteGroup: 'Jannie Mouton',
      totalChildren: 2034,
      totalMeasurements: 2034,
      avgZScore: -0.55,
      stuntingRate: 11.8,
      severeStuntingRate: 3.6,
      atRiskRate: 9.9,
      households: 12,
      temporalData: [
        { period: 'Q1 2021', measurements: 280, avgZScore: -0.68, stunting: 15.2, severeStunting: 5.8 },
        { period: 'Q2 2021', measurements: 350, avgZScore: -0.63, stunting: 14.1, severeStunting: 5.1 },
        { period: 'Q3 2021', measurements: 420, avgZScore: -0.59, stunting: 13.2, severeStunting: 4.5 },
        { period: 'Q4 2021', measurements: 380, avgZScore: -0.57, stunting: 12.6, severeStunting: 4.1 },
        { period: 'Q1 2022', measurements: 340, avgZScore: -0.56, stunting: 12.2, severeStunting: 3.8 },
        { period: 'Q2 2022', measurements: 264, avgZScore: -0.55, stunting: 11.8, severeStunting: 3.6 }
      ],
      categoryBreakdown: [
        { category: 'Normal', count: 1519, percentage: 74.7 },
        { category: 'At Risk', count: 201, percentage: 9.9 },
        { category: 'Stunted', count: 240, percentage: 11.8 },
        { category: 'Severely Stunted', count: 73, percentage: 3.6 }
      ]
    }
  };

  const allLocations = Object.keys(locationsData);
  const currentData = locationsData[selectedLocation];

  // Comparison data with other locations
  const comparisonData = allLocations.map(loc => ({
    name: loc === selectedLocation ? `${loc} (Current)` : loc,
    avgZScore: locationsData[loc].avgZScore,
    stuntingRate: locationsData[loc].stuntingRate,
    children: locationsData[loc].totalChildren,
    isCurrent: loc === selectedLocation
  })).sort((a, b) => b.children - a.children);

  // Metric comparison card
  const ComparisonMetric = ({ label, value, unit, rank, total, trend }) => (
    <div style={{
      background: 'white',
      borderRadius: '8px',
      padding: '16px',
      border: '1px solid #E2E8F0'
    }}>
      <div style={{ fontSize: '12px', color: '#718096', marginBottom: '4px', fontWeight: '500' }}>
        {label}
      </div>
      <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#2D3748', marginBottom: '4px' }}>
        {value}{unit}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontSize: '12px', color: '#718096' }}>
          Rank: {rank} of {total}
        </div>
        {trend && (
          <div style={{
            fontSize: '12px',
            fontWeight: '600',
            color: trend > 0 ? '#48BB78' : '#F56565',
            display: 'flex',
            alignItems: 'center',
            gap: '2px'
          }}>
            <TrendingUp size={12} style={{ transform: trend < 0 ? 'rotate(180deg)' : 'none' }} />
            {Math.abs(trend)}%
          </div>
        )}
      </div>
    </div>
  );

  // Calculate rankings
  const zScoreRank = allLocations
    .sort((a, b) => locationsData[b].avgZScore - locationsData[a].avgZScore)
    .indexOf(selectedLocation) + 1;
  
  const stuntingRank = allLocations
    .sort((a, b) => locationsData[a].stuntingRate - locationsData[b].stuntingRate)
    .indexOf(selectedLocation) + 1;

  const childrenRank = allLocations
    .sort((a, b) => locationsData[b].totalChildren - locationsData[a].totalChildren)
    .indexOf(selectedLocation) + 1;

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#2D3748', margin: 0, marginBottom: '8px' }}>
          Location Analysis
        </h1>
        <p style={{ fontSize: '16px', color: '#718096', margin: 0 }}>
          Deep dive into site-specific nutrition outcomes and trends
        </p>
      </div>

      {/* Location Selector */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <label style={{
          fontSize: '14px',
          fontWeight: '600',
          color: '#2D3748',
          marginBottom: '8px',
          display: 'block'
        }}>
          Select Location
        </label>
        <select
          value={selectedLocation}
          onChange={(e) => setSelectedLocation(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            fontSize: '16px',
            border: '2px solid #E2E8F0',
            borderRadius: '8px',
            background: 'white',
            cursor: 'pointer',
            outline: 'none',
            transition: 'border-color 0.2s'
          }}
          onFocus={(e) => e.target.style.borderColor = '#4299E1'}
          onBlur={(e) => e.target.style.borderColor = '#E2E8F0'}
        >
          {allLocations.map(loc => (
            <option key={loc} value={loc}>
              {loc} - {locationsData[loc].totalChildren} children measured
            </option>
          ))}
        </select>
      </div>

      {/* Location Summary Card */}
      <div style={{
        background: 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)',
        borderRadius: '12px',
        padding: '32px',
        marginBottom: '24px',
        color: 'white',
        boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '24px' }}>
          <div>
            <h2 style={{ fontSize: '28px', fontWeight: 'bold', margin: 0, marginBottom: '8px' }}>
              {selectedLocation}
            </h2>
            <div style={{ fontSize: '16px', opacity: 0.9, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <MapPin size={16} />
              Program Partner: {currentData.siteGroup}
            </div>
          </div>
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            padding: '12px 20px',
            borderRadius: '8px',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{ fontSize: '12px', opacity: 0.9, marginBottom: '4px' }}>Total Measurements</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{currentData.totalMeasurements.toLocaleString()}</div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
          <div>
            <div style={{ fontSize: '12px', opacity: 0.8, marginBottom: '4px' }}>Unique Children</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{currentData.totalChildren.toLocaleString()}</div>
          </div>
          <div>
            <div style={{ fontSize: '12px', opacity: 0.8, marginBottom: '4px' }}>Households/Centers</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{currentData.households}</div>
          </div>
          <div>
            <div style={{ fontSize: '12px', opacity: 0.8, marginBottom: '4px' }}>Avg Z-Score</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{currentData.avgZScore.toFixed(2)}</div>
          </div>
          <div>
            <div style={{ fontSize: '12px', opacity: 0.8, marginBottom: '4px' }}>Stunting Rate</div>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{currentData.stuntingRate.toFixed(1)}%</div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div style={{ marginBottom: '24px' }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '16px' }}>
          Performance Metrics vs Other Locations
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
          <ComparisonMetric
            label="Children Measured"
            value={currentData.totalChildren.toLocaleString()}
            unit=""
            rank={childrenRank}
            total={allLocations.length}
          />
          <ComparisonMetric
            label="Avg Z-Score"
            value={currentData.avgZScore.toFixed(2)}
            unit=""
            rank={zScoreRank}
            total={allLocations.length}
            trend={8.5}
          />
          <ComparisonMetric
            label="Stunting Rate"
            value={currentData.stuntingRate.toFixed(1)}
            unit="%"
            rank={stuntingRank}
            total={allLocations.length}
            trend={-12.3}
          />
          <ComparisonMetric
            label="Severe Stunting"
            value={currentData.severeStuntingRate.toFixed(1)}
            unit="%"
            rank={stuntingRank}
            total={allLocations.length}
            trend={-18.7}
          />
        </div>
      </div>

      {/* Temporal Trends for Selected Location */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Nutrition Outcomes Over Time - {selectedLocation}
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={currentData.temporalData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="period" stroke="#718096" />
            <YAxis yAxisId="left" stroke="#718096" label={{ value: 'Stunting %', angle: -90, position: 'insideLeft' }} />
            <YAxis yAxisId="right" orientation="right" stroke="#718096" label={{ value: 'Z-Score', angle: 90, position: 'insideRight' }} domain={[-1, 0]} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
            />
            <Legend />
            <Line yAxisId="left" type="monotone" dataKey="stunting" name="Stunting Rate %" stroke={COLORS.stunted} strokeWidth={3} dot={{ r: 5 }} />
            <Line yAxisId="left" type="monotone" dataKey="severeStunting" name="Severe Stunting %" stroke={COLORS.severelyStunted} strokeWidth={3} dot={{ r: 5 }} />
            <Line yAxisId="right" type="monotone" dataKey="avgZScore" name="Avg Z-Score" stroke={COLORS.primary} strokeWidth={3} dot={{ r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId={`temporal-${selectedLocation}`}
          graphTitle={`Temporal Trends for ${selectedLocation}`}
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

      {/* Number of Children by Stunting Category - First vs Last vs Target */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Number of Children by Stunting Category - {selectedLocation}
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={[
            { 
              measurement: 'First', 
              atRisk: Math.round(currentData.totalChildren * 0.115), 
              stunted: Math.round(currentData.totalChildren * 0.21), 
              severelyStunted: Math.round(currentData.totalChildren * 0.08) 
            },
            { 
              measurement: 'Last', 
              atRisk: Math.round(currentData.totalChildren * (currentData.atRiskRate / 100)), 
              stunted: Math.round(currentData.totalChildren * (currentData.stuntingRate / 100)), 
              severelyStunted: Math.round(currentData.totalChildren * (currentData.severeStuntingRate / 100)) 
            },
            { 
              measurement: 'Target', 
              atRisk: Math.round(currentData.totalChildren * 0.025), 
              stunted: Math.round(currentData.totalChildren * 0.025), 
              severelyStunted: Math.round(currentData.totalChildren * 0.0015) 
            }
          ]}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="measurement" stroke="#718096" />
            <YAxis stroke="#718096" label={{ value: 'Number of Children', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
            />
            <Legend />
            <Bar dataKey="atRisk" name="At Risk" fill={COLORS.atRisk} radius={[8, 8, 0, 0]} />
            <Bar dataKey="stunted" name="Stunted" fill={COLORS.stunted} radius={[8, 8, 0, 0]} />
            <Bar dataKey="severelyStunted" name="Severely Stunted" fill={COLORS.severelyStunted} radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId={`children-measured-${selectedLocation}`}
          graphTitle={`Children by Stunting Category for ${selectedLocation}`}
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

      {/* Category Breakdown */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Current Status Distribution - {selectedLocation}
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={currentData.categoryBreakdown}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="category" stroke="#718096" />
            <YAxis stroke="#718096" label={{ value: 'Number of Children', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
              formatter={(value, name, props) => [
                `${value} children (${props.payload.percentage.toFixed(1)}%)`,
                name
              ]}
            />
            <Bar dataKey="count" radius={[8, 8, 0, 0]}>
              {currentData.categoryBreakdown.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={
                  entry.category === 'Normal' ? COLORS.normal :
                  entry.category === 'At Risk' ? COLORS.atRisk :
                  entry.category === 'Stunted' ? COLORS.stunted :
                  COLORS.severelyStunted
                } />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId={`breakdown-${selectedLocation}`}
          graphTitle={`Status Distribution for ${selectedLocation}`}
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

      {/* Comparative Analysis with All Locations */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Z-Score Comparison Across All Locations
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={comparisonData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis type="number" stroke="#718096" domain={[-1, 0]} />
            <YAxis dataKey="name" type="category" stroke="#718096" width={200} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
              formatter={(value, name) => [value.toFixed(2), 'Avg Z-Score']}
            />
            <Bar dataKey="avgZScore" radius={[0, 8, 8, 0]}>
              {comparisonData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.isCurrent ? '#667EEA' : COLORS.primary}
                  opacity={entry.isCurrent ? 1 : 0.6}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId={`comparison-${selectedLocation}`}
          graphTitle="Cross-Location Comparison"
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

      {/* Stunting Rate Comparison */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Stunting Rate Comparison (Lower is Better)
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={comparisonData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis type="number" stroke="#718096" label={{ value: 'Stunting Rate (%)', position: 'insideBottom', offset: -5 }} />
            <YAxis dataKey="name" type="category" stroke="#718096" width={200} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
              formatter={(value, name) => [`${value.toFixed(1)}%`, 'Stunting Rate']}
            />
            <Bar dataKey="stuntingRate" radius={[0, 8, 8, 0]}>
              {comparisonData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.isCurrent ? '#FC8181' : COLORS.stunted}
                  opacity={entry.isCurrent ? 1 : 0.6}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId={`stunting-comparison-${selectedLocation}`}
          graphTitle="Stunting Rate Comparison"
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

      {/* Measurement Volume Over Time */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
          Measurement Volume Over Time - {selectedLocation}
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <AreaChart data={currentData.temporalData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="period" stroke="#718096" />
            <YAxis stroke="#718096" label={{ value: 'Number of Measurements', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
            />
            <Area 
              type="monotone" 
              dataKey="measurements" 
              stroke={COLORS.secondary} 
              fill={COLORS.secondary} 
              fillOpacity={0.6}
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
        <AIInterpretation 
          graphId={`volume-${selectedLocation}`}
          graphTitle={`Measurement Volume for ${selectedLocation}`}
          loadingAI={loadingAI}
          setLoadingAI={setLoadingAI}
        />
      </div>

    </div>
  );
};

// Child Analysis Page
const ChildPage = () => {
  const [selectedLocation, setSelectedLocation] = useState('Sasolburg');
  const [selectedChild, setSelectedChild] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [loadingAI, setLoadingAI] = useState({});

  const COLORS = {
    atRisk: '#F6AD55',
    stunted: '#FC8181',
    severelyStunted: '#E53E3E',
    normal: '#68D391',
    primary: '#4299E1',
    secondary: '#9F7AEA'
  };

  // Children data by location
  const childrenByLocation = {
    'Sasolburg': [
      { 
        id: 161592, 
        name: 'Onthatile Molefe',
        age: 4.2,
        gender: 'Female',
        householdId: 87234,
        household: 'Ipelegeng ELC (Goratamang)',
        measurements: [
          { date: '2020-11-27', height: 88.5, zScore: -1.2, status: 'At Risk', age: 3.1 },
          { date: '2021-03-15', height: 91.8, zScore: -0.9, status: 'At Risk', age: 3.4 },
          { date: '2021-07-22', height: 94.5, zScore: -0.6, status: 'Normal', age: 3.8 },
          { date: '2021-11-10', height: 96.8, zScore: -0.4, status: 'Normal', age: 4.1 },
          { date: '2022-03-18', height: 99.2, zScore: -0.2, status: 'Normal', age: 4.4 },
          { date: '2022-07-25', height: 101.5, zScore: 0.0, status: 'Normal', age: 4.8 }
        ],
        firstMeasurement: { date: '2020-11-27', height: 88.5, zScore: -1.2, status: 'At Risk' },
        lastMeasurement: { date: '2022-07-25', height: 101.5, zScore: 0.0, status: 'Normal' },
        totalMeasurements: 6,
        avgZScore: -0.55,
        heightGain: 13.0,
        zScoreImprovement: 1.2
      },
      { 
        id: 132465, 
        name: 'Ithandile Nkosi',
        age: 3.8,
        gender: 'Male',
        householdId: 87234,
        household: 'Ipelegeng ELC (Goratamang)',
        measurements: [
          { date: '2020-12-14', height: 85.2, zScore: -1.8, status: 'Stunted', age: 2.9 },
          { date: '2021-04-08', height: 88.1, zScore: -1.5, status: 'At Risk', age: 3.2 },
          { date: '2021-08-19', height: 91.5, zScore: -1.2, status: 'At Risk', age: 3.6 },
          { date: '2021-12-12', height: 94.2, zScore: -0.9, status: 'At Risk', age: 3.9 },
          { date: '2022-04-20', height: 96.8, zScore: -0.6, status: 'Normal', age: 4.2 }
        ],
        firstMeasurement: { date: '2020-12-14', height: 85.2, zScore: -1.8, status: 'Stunted' },
        lastMeasurement: { date: '2022-04-20', height: 96.8, zScore: -0.6, status: 'Normal' },
        totalMeasurements: 5,
        avgZScore: -1.2,
        heightGain: 11.6,
        zScoreImprovement: 1.2
      },
      { 
        id: 145789, 
        name: 'Lerato Dlamini',
        age: 4.5,
        gender: 'Female',
        householdId: 87235,
        household: 'Sunrise ECD Center',
        measurements: [
          { date: '2021-01-15', height: 91.2, zScore: -0.8, status: 'At Risk', age: 3.2 },
          { date: '2021-05-20', height: 94.5, zScore: -0.5, status: 'Normal', age: 3.6 },
          { date: '2021-09-30', height: 97.8, zScore: -0.3, status: 'Normal', age: 3.9 },
          { date: '2022-02-10', height: 100.5, zScore: -0.1, status: 'Normal', age: 4.3 },
          { date: '2022-06-15', height: 103.2, zScore: 0.1, status: 'Normal', age: 4.6 }
        ],
        firstMeasurement: { date: '2021-01-15', height: 91.2, zScore: -0.8, status: 'At Risk' },
        lastMeasurement: { date: '2022-06-15', height: 103.2, zScore: 0.1, status: 'Normal' },
        totalMeasurements: 5,
        avgZScore: -0.32,
        heightGain: 12.0,
        zScoreImprovement: 0.9
      },
      { 
        id: 156234, 
        name: 'Thabo Mahlangu',
        age: 3.2,
        gender: 'Male',
        householdId: 87236,
        household: 'Rainbow ECD',
        measurements: [
          { date: '2021-06-10', height: 82.5, zScore: -2.3, status: 'Stunted', age: 2.1 },
          { date: '2021-10-15', height: 85.8, zScore: -2.0, status: 'Stunted', age: 2.5 },
          { date: '2022-02-20', height: 88.5, zScore: -1.8, status: 'Stunted', age: 2.8 },
          { date: '2022-06-25', height: 91.2, zScore: -1.5, status: 'At Risk', age: 3.2 }
        ],
        firstMeasurement: { date: '2021-06-10', height: 82.5, zScore: -2.3, status: 'Stunted' },
        lastMeasurement: { date: '2022-06-25', height: 91.2, zScore: -1.5, status: 'At Risk' },
        totalMeasurements: 4,
        avgZScore: -1.9,
        heightGain: 8.7,
        zScoreImprovement: 0.8
      }
    ],
    'Wentworth ECD Forum Durban': [
      { 
        id: 178945, 
        name: 'Amahle Zungu',
        age: 4.8,
        gender: 'Female',
        householdId: 92341,
        household: 'Wentworth Community Center',
        measurements: [
          { date: '2021-02-10', height: 89.5, zScore: -1.5, status: 'At Risk', age: 3.5 },
          { date: '2021-06-18', height: 92.8, zScore: -1.2, status: 'At Risk', age: 3.8 },
          { date: '2021-10-22', height: 95.5, zScore: -0.9, status: 'At Risk', age: 4.2 },
          { date: '2022-03-05', height: 98.2, zScore: -0.6, status: 'Normal', age: 4.5 },
          { date: '2022-07-12', height: 100.8, zScore: -0.3, status: 'Normal', age: 4.9 }
        ],
        firstMeasurement: { date: '2021-02-10', height: 89.5, zScore: -1.5, status: 'At Risk' },
        lastMeasurement: { date: '2022-07-12', height: 100.8, zScore: -0.3, status: 'Normal' },
        totalMeasurements: 5,
        avgZScore: -1.0,
        heightGain: 11.3,
        zScoreImprovement: 1.2
      },
      { 
        id: 189234, 
        name: 'Siyabonga Mthembu',
        age: 3.5,
        gender: 'Male',
        householdId: 92342,
        household: 'Happy Kids ECD',
        measurements: [
          { date: '2021-03-20', height: 84.2, zScore: -2.1, status: 'Stunted', age: 2.4 },
          { date: '2021-07-28', height: 87.5, zScore: -1.8, status: 'Stunted', age: 2.8 },
          { date: '2021-11-30', height: 90.2, zScore: -1.5, status: 'At Risk', age: 3.1 },
          { date: '2022-04-08', height: 93.0, zScore: -1.2, status: 'At Risk', age: 3.5 }
        ],
        firstMeasurement: { date: '2021-03-20', height: 84.2, zScore: -2.1, status: 'Stunted' },
        lastMeasurement: { date: '2022-04-08', height: 93.0, zScore: -1.2, status: 'At Risk' },
        totalMeasurements: 4,
        avgZScore: -1.65,
        heightGain: 8.8,
        zScoreImprovement: 0.9
      }
    ],
    'Kuyasa': [
      { 
        id: 196745, 
        name: 'Naledi Mokoena',
        age: 4.0,
        gender: 'Female',
        householdId: 78456,
        household: 'Kuyasa Development Center',
        measurements: [
          { date: '2020-11-27', height: 87.3, zScore: -1.1, status: 'At Risk', age: 3.0 },
          { date: '2021-03-15', height: 90.5, zScore: -0.8, status: 'At Risk', age: 3.3 },
          { date: '2021-07-22', height: 93.8, zScore: -0.5, status: 'Normal', age: 3.7 },
          { date: '2021-11-10', height: 96.3, zScore: -0.2, status: 'Normal', age: 4.0 },
          { date: '2022-03-18', height: 99.0, zScore: 0.0, status: 'Normal', age: 4.3 }
        ],
        firstMeasurement: { date: '2020-11-27', height: 87.3, zScore: -1.1, status: 'At Risk' },
        lastMeasurement: { date: '2022-03-18', height: 99.0, zScore: 0.0, status: 'Normal' },
        totalMeasurements: 5,
        avgZScore: -0.52,
        heightGain: 11.7,
        zScoreImprovement: 1.1
      }
    ]
  };

  // Get children for selected location
  const availableChildren = childrenByLocation[selectedLocation] || [];
  const filteredChildren = searchTerm 
    ? availableChildren.filter(child => 
        child.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        child.id.toString().includes(searchTerm)
      )
    : availableChildren;

  // Get selected child data
  const childData = availableChildren.find(child => child.id === parseInt(selectedChild));

  // Status badge component
  const StatusBadge = ({ status }) => {
    const colors = {
      'Normal': { bg: '#C6F6D5', text: '#22543D', icon: <CheckCircle size={14} /> },
      'At Risk': { bg: '#FEEBC8', text: '#7C2D12', icon: <AlertCircle size={14} /> },
      'Stunted': { bg: '#FED7D7', text: '#742A2A', icon: <AlertCircle size={14} /> },
      'Severely Stunted': { bg: '#FED7D7', text: '#742A2A', icon: <AlertCircle size={14} /> }
    };
    
    const style = colors[status] || colors['Normal'];
    
    return (
      <span style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '4px',
        padding: '4px 12px',
        background: style.bg,
        color: style.text,
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: '600'
      }}>
        {style.icon}
        {status}
      </span>
    );
  };

  // Alert card component
  const AlertCard = ({ type, title, message }) => {
    const styles = {
      success: { bg: '#C6F6D5', border: '#68D391', icon: '✅', color: '#22543D' },
      warning: { bg: '#FEEBC8', border: '#F6AD55', icon: '⚠️', color: '#7C2D12' },
      info: { bg: '#BEE3F8', border: '#4299E1', icon: 'ℹ️', color: '#2C5282' }
    };
    
    const style = styles[type] || styles.info;
    
    return (
      <div style={{
        background: style.bg,
        border: `2px solid ${style.border}`,
        borderRadius: '8px',
        padding: '16px',
        marginBottom: '16px'
      }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
          <span style={{ fontSize: '24px' }}>{style.icon}</span>
          <div>
            <div style={{ fontWeight: '600', color: style.color, marginBottom: '4px' }}>
              {title}
            </div>
            <div style={{ fontSize: '14px', color: style.color, lineHeight: '1.5' }}>
              {message}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#2D3748', margin: 0, marginBottom: '8px' }}>
          Individual Child Analysis
        </h1>
        <p style={{ fontSize: '16px', color: '#718096', margin: 0 }}>
          Track individual child growth trajectories and nutrition outcomes
        </p>
      </div>

      {/* Selection Panel */}
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        marginBottom: '24px',
        border: '1px solid #E2E8F0'
      }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          {/* Location Selector */}
          <div>
            <label style={{
              fontSize: '14px',
              fontWeight: '600',
              color: '#2D3748',
              marginBottom: '8px',
              display: 'block'
            }}>
              Select Location
            </label>
            <select
              value={selectedLocation}
              onChange={(e) => {
                setSelectedLocation(e.target.value);
                setSelectedChild('');
                setSearchTerm('');
              }}
              style={{
                width: '100%',
                padding: '12px 16px',
                fontSize: '16px',
                border: '2px solid #E2E8F0',
                borderRadius: '8px',
                background: 'white',
                cursor: 'pointer',
                outline: 'none'
              }}
            >
              {Object.keys(childrenByLocation).map(loc => (
                <option key={loc} value={loc}>
                  {loc} - {childrenByLocation[loc].length} children
                </option>
              ))}
            </select>
          </div>

          {/* Child Selector */}
          <div>
            <label style={{
              fontSize: '14px',
              fontWeight: '600',
              color: '#2D3748',
              marginBottom: '8px',
              display: 'block'
            }}>
              Select Child
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                placeholder="Search by name or ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  fontSize: '16px',
                  border: '2px solid #E2E8F0',
                  borderRadius: '8px',
                  outline: 'none',
                  marginBottom: '8px'
                }}
              />
              <select
                value={selectedChild}
                onChange={(e) => setSelectedChild(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  fontSize: '16px',
                  border: '2px solid #E2E8F0',
                  borderRadius: '8px',
                  background: 'white',
                  cursor: 'pointer',
                  outline: 'none'
                }}
              >
                <option value="">-- Select a child --</option>
                {filteredChildren.map(child => (
                  <option key={child.id} value={child.id}>
                    {child.name} (ID: {child.id})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Child Profile (only shown when child is selected) */}
      {childData ? (
        <>
          {/* Child Summary Card */}
          <div style={{
            background: 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)',
            borderRadius: '12px',
            padding: '32px',
            marginBottom: '24px',
            color: 'white',
            boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
              <div>
                <div style={{ fontSize: '12px', opacity: 0.9, marginBottom: '4px' }}>
                  BENEFICIARY ID: {childData.id}
                </div>
                <h2 style={{ fontSize: '32px', fontWeight: 'bold', margin: 0, marginBottom: '12px' }}>
                  {childData.name}
                </h2>
                <div style={{ display: 'flex', gap: '24px', fontSize: '16px', opacity: 0.95 }}>
                  <div>
                    <span style={{ opacity: 0.8 }}>Age:</span> <strong>{childData.age} years</strong>
                  </div>
                  <div>
                    <span style={{ opacity: 0.8 }}>Gender:</span> <strong>{childData.gender}</strong>
                  </div>
                  <div>
                    <span style={{ opacity: 0.8 }}>Measurements:</span> <strong>{childData.totalMeasurements}</strong>
                  </div>
                </div>
                <div style={{ marginTop: '12px', fontSize: '14px', opacity: 0.9 }}>
                  <MapPin size={14} style={{ display: 'inline', marginRight: '6px' }} />
                  {childData.household}
                </div>
              </div>
              
              <div style={{ textAlign: 'right' }}>
                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '16px 24px',
                  borderRadius: '12px',
                  backdropFilter: 'blur(10px)',
                  marginBottom: '12px'
                }}>
                  <div style={{ fontSize: '12px', opacity: 0.9, marginBottom: '4px' }}>Current Status</div>
                  <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
                    {childData.lastMeasurement.status}
                  </div>
                </div>
                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '12px 24px',
                  borderRadius: '12px',
                  backdropFilter: 'blur(10px)'
                }}>
                  <div style={{ fontSize: '12px', opacity: 0.9, marginBottom: '4px' }}>Latest Z-Score</div>
                  <div style={{ fontSize: '20px', fontWeight: 'bold' }}>
                    {childData.lastMeasurement.zScore.toFixed(2)}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Progress Indicators */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
            <div style={{
              background: 'white',
              borderRadius: '8px',
              padding: '20px',
              border: '1px solid #E2E8F0'
            }}>
              <div style={{ fontSize: '12px', color: '#718096', marginBottom: '8px', fontWeight: '500' }}>
                Height Gain
              </div>
              <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#2D3748', marginBottom: '4px' }}>
                +{childData.heightGain.toFixed(1)} cm
              </div>
              <div style={{ fontSize: '12px', color: '#48BB78', fontWeight: '600' }}>
                ↑ First to Last
              </div>
            </div>

            <div style={{
              background: 'white',
              borderRadius: '8px',
              padding: '20px',
              border: '1px solid #E2E8F0'
            }}>
              <div style={{ fontSize: '12px', color: '#718096', marginBottom: '8px', fontWeight: '500' }}>
                Z-Score Improvement
              </div>
              <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#2D3748', marginBottom: '4px' }}>
                +{childData.zScoreImprovement.toFixed(2)}
              </div>
              <div style={{ fontSize: '12px', color: '#48BB78', fontWeight: '600' }}>
                ↑ Positive Trend
              </div>
            </div>

            <div style={{
              background: 'white',
              borderRadius: '8px',
              padding: '20px',
              border: '1px solid #E2E8F0'
            }}>
              <div style={{ fontSize: '12px', color: '#718096', marginBottom: '8px', fontWeight: '500' }}>
                Average Z-Score
              </div>
              <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#2D3748', marginBottom: '4px' }}>
                {childData.avgZScore.toFixed(2)}
              </div>
              <div style={{ fontSize: '12px', color: '#718096', fontWeight: '500' }}>
                Across all measurements
              </div>
            </div>

            <div style={{
              background: 'white',
              borderRadius: '8px',
              padding: '20px',
              border: '1px solid #E2E8F0'
            }}>
              <div style={{ fontSize: '12px', color: '#718096', marginBottom: '8px', fontWeight: '500' }}>
                Monitoring Period
              </div>
              <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#2D3748', marginBottom: '4px' }}>
                {Math.round((new Date(childData.lastMeasurement.date) - new Date(childData.firstMeasurement.date)) / (1000 * 60 * 60 * 24 * 30))} mo
              </div>
              <div style={{ fontSize: '12px', color: '#718096', fontWeight: '500' }}>
                {childData.totalMeasurements} measurements
              </div>
            </div>
          </div>

          {/* Progress Alert */}
          {childData.lastMeasurement.status === 'Normal' && childData.firstMeasurement.status !== 'Normal' && (
            <AlertCard
              type="success"
              title="Excellent Progress!"
              message={`${childData.name} has successfully moved from "${childData.firstMeasurement.status}" to "Normal" status. The Z-score improved by ${childData.zScoreImprovement.toFixed(2)} points, indicating effective nutritional intervention.`}
            />
          )}

          {childData.lastMeasurement.status === 'At Risk' && childData.firstMeasurement.status === 'Stunted' && (
            <AlertCard
              type="warning"
              title="Positive Trend, Continued Monitoring Needed"
              message={`${childData.name} has improved from "Stunted" to "At Risk" status. Continue current interventions and monitor closely to achieve "Normal" status.`}
            />
          )}

          {childData.lastMeasurement.status === 'Stunted' && (
            <AlertCard
              type="warning"
              title="Requires Attention"
              message={`${childData.name} is currently classified as "${childData.lastMeasurement.status}". Enhanced nutritional support and regular monitoring are recommended.`}
            />
          )}

          {/* Growth Trajectory Chart */}
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '24px',
            border: '1px solid #E2E8F0'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
              Height Growth Trajectory - {childData.name}
            </h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={childData.measurements}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="date" stroke="#718096" />
                <YAxis 
                  stroke="#718096" 
                  label={{ value: 'Height (cm)', angle: -90, position: 'insideLeft' }}
                  domain={[80, 110]}
                />
                <Tooltip 
                  contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
                  formatter={(value, name) => {
                    if (name === 'height') return [`${value} cm`, 'Height'];
                    return [value, name];
                  }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="height" 
                  stroke={COLORS.primary} 
                  strokeWidth={3} 
                  dot={{ r: 6, fill: COLORS.primary }}
                  name="Height (cm)"
                />
              </LineChart>
            </ResponsiveContainer>
            <AIInterpretation 
              graphId={`growth-${childData.id}`}
              graphTitle={`Growth Trajectory for ${childData.name}`}
              loadingAI={loadingAI}
              setLoadingAI={setLoadingAI}
            />
          </div>

          {/* Z-Score Progression Chart */}
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '24px',
            border: '1px solid #E2E8F0'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
              WHO Z-Score Progression - {childData.name}
            </h3>
            <div style={{ 
              marginBottom: '16px', 
              padding: '12px', 
              background: '#EBF8FF', 
              borderRadius: '8px', 
              fontSize: '14px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <div>
                <strong>WHO Normal Range:</strong> -2 to +2 • <strong>Target:</strong> 0
              </div>
              <div style={{ display: 'flex', gap: '12px', fontSize: '12px' }}>
                <span style={{ color: '#E53E3E' }}>■ Severely Stunted (&lt; -3)</span>
                <span style={{ color: '#FC8181' }}>■ Stunted (-3 to -2)</span>
                <span style={{ color: '#F6AD55' }}>■ At Risk (-2 to -1)</span>
                <span style={{ color: '#68D391' }}>■ Normal (-1 to +2)</span>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={childData.measurements}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="date" stroke="#718096" />
                <YAxis 
                  stroke="#718096" 
                  label={{ value: 'Z-Score', angle: -90, position: 'insideLeft' }}
                  domain={[-3, 1]}
                />
                <Tooltip 
                  contentStyle={{ background: 'white', border: '1px solid #E2E8F0', borderRadius: '8px' }}
                  formatter={(value, name, props) => {
                    if (name === 'zScore') {
                      return [`${value.toFixed(2)} (${props.payload.status})`, 'Z-Score'];
                    }
                    return [value, name];
                  }}
                />
                <Legend />
                {/* Reference lines for WHO thresholds */}
                <Line type="monotone" dataKey={() => -2} stroke="#FC8181" strokeDasharray="5 5" strokeWidth={2} name="Stunting Threshold (-2)" dot={false} />
                <Line type="monotone" dataKey={() => -3} stroke="#E53E3E" strokeDasharray="5 5" strokeWidth={2} name="Severe Stunting (-3)" dot={false} />
                <Line type="monotone" dataKey={() => 0} stroke="#48BB78" strokeDasharray="5 5" strokeWidth={2} name="WHO Median (0)" dot={false} />
                <Area 
                  type="monotone" 
                  dataKey="zScore" 
                  stroke={COLORS.secondary} 
                  fill={COLORS.secondary}
                  fillOpacity={0.4}
                  strokeWidth={3}
                  dot={{ r: 6 }}
                  name="Child's Z-Score"
                />
              </AreaChart>
            </ResponsiveContainer>
            <AIInterpretation 
              graphId={`zscore-${childData.id}`}
              graphTitle={`Z-Score Progression for ${childData.name}`}
              loadingAI={loadingAI}
              setLoadingAI={setLoadingAI}
            />
          </div>

          {/* Measurement History Table */}
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '24px',
            border: '1px solid #E2E8F0'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
              Measurement History
            </h3>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: '#F7FAFC', borderBottom: '2px solid #E2E8F0' }}>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600', color: '#2D3748' }}>
                      Date
                    </th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600', color: '#2D3748' }}>
                      Age (years)
                    </th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600', color: '#2D3748' }}>
                      Height (cm)
                    </th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600', color: '#2D3748' }}>
                      Z-Score
                    </th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600', color: '#2D3748' }}>
                      Status
                    </th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600', color: '#2D3748' }}>
                      Change
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {childData.measurements.map((measurement, index) => {
                    const prevMeasurement = index > 0 ? childData.measurements[index - 1] : null;
                    const heightChange = prevMeasurement ? measurement.height - prevMeasurement.height : null;
                    const zScoreChange = prevMeasurement ? measurement.zScore - prevMeasurement.zScore : null;

                    return (
                      <tr key={index} style={{ borderBottom: '1px solid #E2E8F0' }}>
                        <td style={{ padding: '12px', fontSize: '14px', color: '#2D3748' }}>
                          {new Date(measurement.date).toLocaleDateString('en-US', { 
                            year: 'numeric', 
                            month: 'short', 
                            day: 'numeric' 
                          })}
                        </td>
                        <td style={{ padding: '12px', fontSize: '14px', color: '#2D3748' }}>
                          {measurement.age.toFixed(1)}
                        </td>
                        <td style={{ padding: '12px', fontSize: '14px', color: '#2D3748', fontWeight: '600' }}>
                          {measurement.height} cm
                        </td>
                        <td style={{ padding: '12px', fontSize: '14px', color: '#2D3748', fontWeight: '600' }}>
                          {measurement.zScore.toFixed(2)}
                        </td>
                        <td style={{ padding: '12px' }}>
                          <StatusBadge status={measurement.status} />
                        </td>
                        <td style={{ padding: '12px', fontSize: '14px' }}>
                          {heightChange !== null ? (
                            <div>
                              <div style={{ color: '#48BB78', fontWeight: '600' }}>
                                +{heightChange.toFixed(1)} cm
                              </div>
                              <div style={{ color: zScoreChange >= 0 ? '#48BB78' : '#F56565', fontSize: '12px' }}>
                                {zScoreChange >= 0 ? '+' : ''}{zScoreChange.toFixed(2)} z
                              </div>
                            </div>
                          ) : (
                            <span style={{ color: '#A0AEC0', fontSize: '12px' }}>First measurement</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* AI Progress Summary */}
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '24px',
            border: '1px solid #E2E8F0'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#2D3748', marginBottom: '20px' }}>
              AI-Generated Progress Summary
            </h3>
            <AIInterpretation 
              graphId={`summary-${childData.id}`}
              graphTitle={`Overall Progress Summary for ${childData.name}`}
              loadingAI={loadingAI}
              setLoadingAI={setLoadingAI}
            />
          </div>

        </>
      ) : (
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '48px',
          textAlign: 'center',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          border: '1px solid #E2E8F0'
        }}>
          <Users size={64} color="#CBD5E0" style={{ marginBottom: '16px' }} />
          <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#2D3748', marginBottom: '8px' }}>
            Select a Child to View Analysis
          </h3>
          <p style={{ fontSize: '16px', color: '#718096' }}>
            Choose a location and child from the dropdowns above to view detailed growth tracking and nutrition outcomes.
          </p>
        </div>
      )}
    </div>
  );
};

export default ChildNutritionDashboard;
