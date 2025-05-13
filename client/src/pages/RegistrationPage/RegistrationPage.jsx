import React, { useState } from 'react';
import './RegistrationPage.scss';

const BLINDNESS = "BLINDNESS";
const WHEELCHAIR = "WHEELCHAIR";

const RegistrationPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    disabilityType: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};
    if (!formData.name.trim()) {
      newErrors.name = 'Имя обязательно';
    }
    if (!/^\S+@\S+\.\S+$/.test(formData.email)) {
      newErrors.email = 'Некорректный email';
    }
    if (formData.password.length < 6) {
      newErrors.password = 'Пароль должен быть не менее 6 символов';
    }
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Пароли не совпадают';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      const response = await fetch('http://localhost:5000/auth/registration', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          full_name: formData.name,
          email: formData.email,
          password: formData.password,
          problem_type: formData.disabilityType
        }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'Ошибка регистрации');
      }

      
      window.location.href = '/';
    } catch (error) {
      setErrors({...errors, server: error.message});
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="registration-container">
      <form className="registration-form" onSubmit={handleSubmit} noValidate>
        <h1 className="form-title">Регистрация</h1>
        
        {errors.server && <div className="server-error">{errors.server}</div>}

        <div className="form-group">
          <label htmlFor="name">ФИО</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            disabled={isSubmitting}
            className={errors.name ? 'error' : ''}
          />
          {errors.name && <span className="error-message">{errors.name}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            disabled={isSubmitting}
            className={errors.email ? 'error' : ''}
          />
          {errors.email && <span className="error-message">{errors.email}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="password">Пароль</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            disabled={isSubmitting}
            className={errors.password ? 'error' : ''}
          />
          {errors.password && <span className="error-message">{errors.password}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="confirmPassword">Подтвердите пароль</label>
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            disabled={isSubmitting}
            className={errors.confirmPassword ? 'error' : ''}
          />
          {errors.confirmPassword && 
            <span className="error-message">{errors.confirmPassword}</span>}
        </div>

        <div className="form-group">
          <label>Особенности</label>
          <div className="radio-group">
            <label>
              <input
                type="radio"
                name="disabilityType"
                value={BLINDNESS}
                checked={formData.disabilityType === BLINDNESS}
                onChange={handleChange}
                disabled={isSubmitting}
              />
              Слабовидящий
            </label>
            <label>
              <input
                type="radio"
                name="disabilityType"
                value={WHEELCHAIR}
                checked={formData.disabilityType === WHEELCHAIR}
                onChange={handleChange}
                disabled={isSubmitting}
              />
              Колясочник
            </label>
          </div>
        </div>

        <button 
          type="submit" 
          className="submit-btn"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Регистрация...' : 'Зарегистрироваться'}
        </button>

        <div className="login-link">
          Уже есть аккаунт? <a href="/">Войти</a>
        </div>
      </form>
    </div>
  );
};

export default RegistrationPage;