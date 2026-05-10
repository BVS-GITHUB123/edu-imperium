import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import './App.css';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/* ─── tiny helpers ─────────────────────────────────────────────────────── */
const levelColor = { beginner: '#10b981', intermediate: '#f59e0b', advanced: '#ef4444' };
const levelBg   = { beginner: '#052e16', intermediate: '#451a03', advanced: '#450a0a' };
const fmt = n => n >= 1000 ? `${(n / 1000).toFixed(1)}k` : n;

/* ─── Navbar ────────────────────────────────────────────────────────────── */
function Navbar({ onEnrollClick }) {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', h);
    return () => window.removeEventListener('scroll', h);
  }, []);
  return (
    <nav className={`navbar ${scrolled ? 'navbar--scrolled' : ''}`}>
      <div className="nav-inner">
        <div className="nav-brand">
          <span className="brand-icon">⚡</span>
          <span className="brand-name">EduImperium</span>
        </div>
        <div className="nav-links">
          <a href="#courses" className="nav-link">Courses</a>
          <a href="#stats" className="nav-link">Stats</a>
          <button className="btn btn-primary btn-sm" onClick={onEnrollClick}>
            Enroll Now
          </button>
        </div>
      </div>
    </nav>
  );
}

/* ─── Hero ──────────────────────────────────────────────────────────────── */
function Hero({ stats, onExplore }) {
  return (
    <section className="hero">
      <div className="hero-bg">
        <div className="hero-orb orb-1" />
        <div className="hero-orb orb-2" />
        <div className="hero-grid" />
      </div>
      <div className="hero-content">
        <div className="hero-badge">🚀 &nbsp;#1 Online Learning Platform</div>
        <h1 className="hero-title">
          Learn Without <span className="gradient-text">Limits</span>
        </h1>
        <p className="hero-subtitle">
          Master in-demand skills with world-class instructors. Join{' '}
          <strong>{stats ? fmt(stats.total_students) : '…'}</strong> learners
          already transforming their careers.
        </p>
        <div className="hero-actions">
          <button className="btn btn-primary btn-lg" onClick={onExplore}>
            Browse Courses
          </button>
          <a href="#stats" className="btn btn-ghost btn-lg">See Outcomes →</a>
        </div>
        {stats && (
          <div className="hero-chips">
            <span className="chip">📚 {stats.total_courses} Courses</span>
            <span className="chip">🎓 {fmt(stats.total_students)} Students</span>
            <span className="chip">🏷️ {stats.total_categories} Categories</span>
          </div>
        )}
      </div>
    </section>
  );
}

/* ─── Stats Bar ─────────────────────────────────────────────────────────── */
function StatsBar({ stats }) {
  const items = stats ? [
    { label: 'Total Courses',      value: stats.total_courses,    icon: '📚' },
    { label: 'Active Students',    value: fmt(stats.total_students), icon: '🎓' },
    { label: 'Categories',         value: stats.total_categories, icon: '🏷️' },
    { label: 'Featured Courses',   value: stats.featured_count,   icon: '⭐' },
  ] : [];
  return (
    <section className="stats-bar" id="stats">
      <div className="container">
        <div className="stats-grid">
          {items.map(s => (
            <div className="stat-card" key={s.label}>
              <span className="stat-icon">{s.icon}</span>
              <span className="stat-value">{s.value}</span>
              <span className="stat-label">{s.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ─── Filter Bar ────────────────────────────────────────────────────────── */
function FilterBar({ categories, filters, onChange }) {
  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label className="filter-label">Category</label>
        <select
          className="filter-select"
          value={filters.category}
          onChange={e => onChange({ ...filters, category: e.target.value })}
        >
          <option value="">All Categories</option>
          {categories.map(c => (
            <option key={c.id} value={c.id}>{c.icon} {c.name}</option>
          ))}
        </select>
      </div>
      <div className="filter-group">
        <label className="filter-label">Level</label>
        <select
          className="filter-select"
          value={filters.level}
          onChange={e => onChange({ ...filters, level: e.target.value })}
        >
          <option value="">All Levels</option>
          <option value="beginner">🟢 Beginner</option>
          <option value="intermediate">🟡 Intermediate</option>
          <option value="advanced">🔴 Advanced</option>
        </select>
      </div>
      <div className="filter-group">
        <label className="filter-label">Sort By</label>
        <select
          className="filter-select"
          value={filters.ordering}
          onChange={e => onChange({ ...filters, ordering: e.target.value })}
        >
          <option value="-created_at">Newest</option>
          <option value="-rating">Top Rated</option>
          <option value="-students_enrolled">Most Popular</option>
          <option value="price">Price: Low to High</option>
          <option value="-price">Price: High to Low</option>
        </select>
      </div>
      <div className="filter-group search-group">
        <label className="filter-label">Search</label>
        <input
          className="filter-input"
          placeholder="Search courses…"
          value={filters.search}
          onChange={e => onChange({ ...filters, search: e.target.value })}
        />
      </div>
    </div>
  );
}

/* ─── Course Card ───────────────────────────────────────────────────────── */
function CourseCard({ course, onEnroll }) {
  const stars = Math.round(Number(course.rating));
  return (
    <article className="course-card">
      <div className="course-card-header">
        <span className="course-category-icon">{course.category?.icon || '📚'}</span>
        <span
          className="course-level"
          style={{ color: levelColor[course.level], background: levelBg[course.level] }}
        >
          {course.level}
        </span>
        {course.is_featured && <span className="course-featured">⭐ Featured</span>}
      </div>
      <div className="course-card-body">
        <h3 className="course-title">{course.title}</h3>
        <p className="course-desc">{course.description}</p>
        <p className="course-instructor">
          <span className="instructor-avatar">{course.instructor[0]}</span>
          {course.instructor}
        </p>
      </div>
      <div className="course-card-footer">
        <div className="course-meta">
          <span className="meta-item">
            {'★'.repeat(stars)}{'☆'.repeat(5 - stars)}
            <span className="meta-val">{Number(course.rating).toFixed(1)}</span>
          </span>
          <span className="meta-item">⏱ {course.duration_hours}h</span>
          <span className="meta-item">👥 {fmt(course.students_enrolled)}</span>
        </div>
        <div className="course-bottom">
          <span className="course-price">
            {Number(course.price) === 0 ? 'Free' : `₹${Number(course.price).toLocaleString()}`}
          </span>
          <button className="btn btn-primary btn-sm" onClick={() => onEnroll(course)}>
            Enroll
          </button>
        </div>
      </div>
    </article>
  );
}

/* ─── Enroll Modal ──────────────────────────────────────────────────────── */
function EnrollModal({ course, onClose }) {
  const [form, setForm] = useState({ name: '', email: '' });
  const [status, setStatus] = useState('idle'); // idle | loading | success | error
  const [msg, setMsg] = useState('');

  const submit = async e => {
    e.preventDefault();
    setStatus('loading');
    try {
      await axios.post(`${API}/api/enroll/`, {
        name: form.name,
        email: form.email,
        course: course.id,
      });
      setStatus('success');
      setMsg(`🎉 You're enrolled in "${course.title}"!`);
    } catch (err) {
      setStatus('error');
      const data = err?.response?.data;
      if (typeof data === 'object') {
        setMsg(Object.values(data).flat().join(' '));
      } else {
        setMsg('Something went wrong. Please try again.');
      }
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>
        <div className="modal-header">
          <span className="modal-icon">{course.category?.icon || '📚'}</span>
          <h2 className="modal-title">Enroll in Course</h2>
          <p className="modal-course">{course.title}</p>
        </div>
        {status === 'success' ? (
          <div className="modal-success">
            <div className="success-circle">✓</div>
            <p>{msg}</p>
            <button className="btn btn-primary" onClick={onClose}>Back to Courses</button>
          </div>
        ) : (
          <form className="modal-form" onSubmit={submit}>
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <input
                id="enroll-name"
                className="form-input"
                placeholder="Your name"
                required
                value={form.name}
                onChange={e => setForm({ ...form, name: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Email Address</label>
              <input
                id="enroll-email"
                type="email"
                className="form-input"
                placeholder="you@example.com"
                required
                value={form.email}
                onChange={e => setForm({ ...form, email: e.target.value })}
              />
            </div>
            {status === 'error' && <p className="form-error">{msg}</p>}
            <button
              id="enroll-submit"
              type="submit"
              className="btn btn-primary btn-full"
              disabled={status === 'loading'}
            >
              {status === 'loading' ? 'Enrolling…' : 'Confirm Enrollment'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

/* ─── App ───────────────────────────────────────────────────────────────── */
export default function App() {
  const [stats, setStats]           = useState(null);
  const [categories, setCategories] = useState([]);
  const [courses, setCourses]       = useState([]);
  const [loading, setLoading]       = useState(true);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [filters, setFilters] = useState({
    category: '', level: '', ordering: '-created_at', search: '',
  });

  /* fetch stats + categories once */
  useEffect(() => {
    axios.get(`${API}/api/stats/`).then(r => setStats(r.data)).catch(() => {});
    axios.get(`${API}/api/categories/`).then(r => setCategories(r.data)).catch(() => {});
  }, []);

  /* fetch courses on filter change */
  const fetchCourses = useCallback(() => {
    setLoading(true);
    const params = {};
    if (filters.category) params.category = filters.category;
    if (filters.level)    params.level    = filters.level;
    if (filters.ordering) params.ordering = filters.ordering;
    if (filters.search)   params.search   = filters.search;
    axios
      .get(`${API}/api/courses/`, { params })
      .then(r => { setCourses(r.data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [filters]);

  useEffect(() => { fetchCourses(); }, [fetchCourses]);

  const scrollToCourses = () =>
    document.getElementById('courses')?.scrollIntoView({ behavior: 'smooth' });

  return (
    <div className="app">
      <Navbar onEnrollClick={scrollToCourses} />
      <Hero stats={stats} onExplore={scrollToCourses} />
      <StatsBar stats={stats} />

      {/* Courses Section */}
      <section className="courses-section" id="courses">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">
              Explore <span className="gradient-text">Courses</span>
            </h2>
            <p className="section-subtitle">
              Hand-picked courses from industry experts across every domain
            </p>
          </div>
          <FilterBar categories={categories} filters={filters} onChange={setFilters} />
          {loading ? (
            <div className="loading-grid">
              {[...Array(6)].map((_, i) => <div key={i} className="skeleton-card" />)}
            </div>
          ) : courses.length === 0 ? (
            <div className="empty-state">
              <span className="empty-icon">🔍</span>
              <p>No courses match your filters. Try adjusting them.</p>
            </div>
          ) : (
            <div className="courses-grid">
              {courses.map(c => (
                <CourseCard key={c.id} course={c} onEnroll={setSelectedCourse} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container footer-inner">
          <div className="footer-brand">
            <span className="brand-icon">⚡</span>
            <span className="brand-name">EduImperium</span>
          </div>
          <p className="footer-copy">© 2026 EduImperium. Built with Django &amp; React.</p>
        </div>
      </footer>

      {selectedCourse && (
        <EnrollModal
          course={selectedCourse}
          onClose={() => setSelectedCourse(null)}
        />
      )}
    </div>
  );
}
