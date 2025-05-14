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
  const [errors, setErrors] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const validateForm = () => {
    const errorMessages = [];
    
    if (!formData.name.trim()) {
      errorMessages.push('Имя обязательно');
    }
    if (!/^\S+@\S+\.\S+$/.test(formData.email)) {
      errorMessages.push('Некорректный email');
    }
    if (formData.password.length < 6) {
      errorMessages.push('Пароль должен быть не менее 6 символов');
    }
    if (formData.password !== formData.confirmPassword) {
      errorMessages.push('Пароли не совпадают');
    }
    
    setErrors(errorMessages);
    return errorMessages.length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) {
      setIsModalOpen(true);
      return;
    }

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
      setErrors([error.message]);
      setIsModalOpen(true);
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

  const closeModal = () => {
    setIsModalOpen(false);
    setErrors([]);
  };

  return (
    <div className="registration-container">
      <form className="registration-form" onSubmit={handleSubmit} noValidate>
        <h1 className="form-title">Регистрация</h1>

        <div className="form-group">
          <label htmlFor="name">ФИО</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            disabled={isSubmitting}
          />
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
          />
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
          />
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
          />
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

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="error-modal">
            <div className="modal-header">
              <h3>Ошибка</h3>
              <button className="close-btn" onClick={closeModal}>&times;</button>
            </div>
            <div className="modal-content">
              {errors.map((error, index) => (
                <p key={index} className="error-message">{error}</p>
              ))}
            </div>
            <button className="modal-close-btn" onClick={closeModal}>
              Закрыть
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RegistrationPage;