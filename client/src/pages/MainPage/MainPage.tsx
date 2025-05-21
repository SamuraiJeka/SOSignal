import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './MainPage.scss';
import React from 'react';

interface Order {
  baggage: boolean;
  order_date: string;
  start_time: string;
  finish_time: string;
  id: number;
  user_id: number;
  staff?: Staff[];
}

interface Staff {
  full_name: string;
  email: string;
}

interface Staff {
  id: number;
  name: string;
  position: string;
  email: string;
}

interface NewOrder {
  baggage: boolean;
  order_date: string;
  start_time: string;
  finish_time: string;
}

const API_BASE_URL = 'http://localhost:5000';

const MainPage = () => {
  const navigate = useNavigate();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newOrder, setNewOrder] = useState<NewOrder>({
    baggage: false,
    order_date: new Date().toISOString().split('T')[0],
    start_time: '12:00',
    finish_time: '13:00'
  });
  const [expandedOrderId, setExpandedOrderId] = useState<number | null>(null);
  const [staffLoading, setStaffLoading] = useState(false);
  const [staffError, setStaffError] = useState('');

  useEffect(() => {
    const checkAuth = () => {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) navigate('/');
    };

    const fetchOrders = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          navigate('/');
          return;
        }

        const response = await fetch(`${API_BASE_URL}/order/user`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });

        if (!response.ok) throw new Error('Failed to fetch orders');
        
        const data = await response.json();
        setOrders(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
    fetchOrders();

    const interval = setInterval(checkAuth, 5000);
    return () => clearInterval(interval);
  }, [navigate]);

  const formatTime = (timeString: string) => {
    const time = new Date(`1970-01-01T${timeString}`);
    return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;
    
    setNewOrder({
      ...newOrder,
      [name]: val
    });
  };

  const formatTimeForApi = (time: string) => {
    const [hours, minutes] = time.split(':');
    return `${hours}:${minutes}:00.000Z`;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/');
        return;
      }

      const requestData = {
        baggage: newOrder.baggage,
        order_date: newOrder.order_date,
        start_time: formatTimeForApi(newOrder.start_time),
        finish_time: formatTimeForApi(newOrder.finish_time)
      };

      const response = await fetch(`${API_BASE_URL}/order`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create order');
      }

      const createdOrder = await response.json();
      setOrders([...orders, createdOrder]);
      setIsModalOpen(false);
      
      setNewOrder({
        baggage: false,
        order_date: new Date().toISOString().split('T')[0],
        start_time: '12:00',
        finish_time: '13:00'
      });
    } catch (err) {
      console.error('Order creation error:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    }
  };

  const handleDelete = async (orderId: number) => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/');
        return;
      }

      const response = await fetch(`${API_BASE_URL}/order/${orderId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });

      if (!response.ok) throw new Error('Failed to delete order');

      setOrders(orders.filter(order => order.id !== orderId));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    }
  };

  const fetchStaff = async (orderId: number) => {
    try {
      setStaffLoading(true);
      setStaffError('');
      
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/');
        return;
      }

      const response = await fetch(`${API_BASE_URL}/order/stuff/${orderId}`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });

      if (!response.ok) throw new Error('Ошибка загрузки данных сотрудников');
      
      const staffData = await response.json();
      
      setOrders(orders.map(order => 
        order.id === orderId ? { ...order, staff: staffData } : order
      ));
      
    } catch (err) {
      setStaffError(err instanceof Error ? err.message : 'Ошибка загрузки');
    } finally {
      setStaffLoading(false);
    }
  };

  const toggleExpand = async (orderId: number) => {
    if (expandedOrderId === orderId) {
      setExpandedOrderId(null);
    } else {
      setExpandedOrderId(orderId);
      if (!orders.find(o => o.id === orderId)?.staff) {
        await fetchStaff(orderId);
      }
    }
  };

  return (
    <div className="main-container">
      <div className="page-header">
        <h1 className="page-title">Ваши бронирования</h1>
        <button 
          className="create-booking-btn"
          onClick={() => setIsModalOpen(true)}
        >
          Создать бронирование
        </button>
      </div>
      
      {loading ? (
        <div className="loading">Загрузка...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : orders.length === 0 ? (
        <div className="no-orders">Бронирования не найдены</div>
      ) : (
        <div className="orders-list">
          {orders.map((order) => (
            <div key={order.id} className="order-card">
              <div className="order-header">
                <h3>Бронь #{order.id}</h3>
                <div className="order-actions">
                  <span className={`badge ${order.baggage ? 'baggage-yes' : 'baggage-no'}`}>
                    {order.baggage ? 'С багажом' : 'Без багажа'}
                  </span>
                  <button 
                    className="delete-btn"
                    onClick={() => handleDelete(order.id)}
                  >
                    Завершить
                  </button>
                </div>
              </div>
              <div className="order-details">
                <p><strong>Дата:</strong> {order.order_date}</p>
                <p><strong>Время:</strong> {formatTime(order.start_time)} - {formatTime(order.finish_time)}</p>
                
                <button 
                  className={`expand-btn ${expandedOrderId === order.id ? 'expanded' : ''}`}
                  onClick={() => toggleExpand(order.id)}
                >
                  {expandedOrderId === order.id ? 'Скрыть сотрудников' : 'Показать сотрудников'}
                </button>

                {expandedOrderId === order.id && (
                  <div className="staff-section">
                    {staffLoading && <div className="loading-staff">Загрузка сотрудников...</div>}
                    {staffError && <div className="error-staff">{staffError}</div>}
    
                    {order.staff && order.staff.length > 0 ? (
                      <div className="staff-list">
                        <h4>Сотрудники:</h4>
                        {order.staff.map((staff, index) => (
                          <div key={`${order.id}-${index}`} className="staff-item">
                            <p><strong>Имя:</strong> {staff.full_name}</p>
                            <p><strong>Email:</strong> {staff.email}</p>
                            {index < order.staff.length - 1 && <hr className="staff-divider" />}
                          </div>
                        ))}
                      </div>
                    ) : (
                      !staffLoading && !staffError && <div className="no-staff">Сотрудники не назначены</div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>Создать новое бронирование</h2>
              <button 
                className="close-btn"
                onClick={() => setIsModalOpen(false)}
              >
                &times;
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>
                  Дата:
                  <input
                    type="date"
                    name="order_date"
                    value={newOrder.order_date}
                    onChange={handleInputChange}
                    required
                  />
                </label>
              </div>
              <div className="form-group">
                <label>
                  Время начала:
                  <input
                    type="time"
                    name="start_time"
                    value={newOrder.start_time}
                    onChange={handleInputChange}
                    required
                  />
                </label>
              </div>
              <div className="form-group">
                <label>
                  Время окончания:
                  <input
                    type="time"
                    name="finish_time"
                    value={newOrder.finish_time}
                    onChange={handleInputChange}
                    required
                  />
                </label>
              </div>
              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="baggage"
                    checked={newOrder.baggage}
                    onChange={handleInputChange}
                  />
                  Багаж
                </label>
              </div>
              {error && <div className="error-message">{error}</div>}
              <button type="submit" className="submit-btn">
                Создать бронирование
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MainPage;