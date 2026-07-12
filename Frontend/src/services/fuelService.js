import api from './api/axios';

/**
 * Fuel/Expense service.
 */
export const getExpenses = async () => {
  const response = await api.get('/finance/expenses');
  return response.data.data.expenses || [];
};

export default { getExpenses };

