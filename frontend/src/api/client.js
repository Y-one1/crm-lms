const API_URL = 'http://localhost:8000';

export async function apiCall(endpoint, options = {}) {
  const url = `${API_URL}${endpoint}`;
  
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

//===============================
// CHILDREN endpoints
//===============================

export function getChildren() {
  return apiCall(`/children/`);
}

export function getChild(childId) {
  return apiCall(`/children/${childId}`);
}

export function createChild(data) {
  return apiCall('/children/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function updateChild(childId, data) {
  return apiCall(`/children/${childId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function deleteChild(childId) {
  return apiCall(`/children/${childId}`, {
    method: 'DELETE',
  });
}

export function getChildNotes(childId, startDate = null, endDate = null) {
  let url = `/children/${childId}/notes/`;
  const params = [];
  if (startDate) params.push(`start_date=${startDate}`);
  if (endDate) params.push(`end_date=${endDate}`);
  if (params.length) url += '?' + params.join('&');
  return apiCall(url);
}

//===============================
// PARENTS endpoints
//===============================

export function getParents() {
  return apiCall(`/parents/`);
}

export function getParent(parentId) {
  return apiCall(`/parents/${parentId}`);
}

export function createParent(data) {
  return apiCall('/parents/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function updateParent(parentId, data) {
  return apiCall(`/parents/${parentId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function deleteParent(parentId) {
  return apiCall(`/parents/${parentId}`, {
    method: 'DELETE',
  });
}

export function getParentNotes(parentId, startDate = null, endDate = null) {
  let url = `/parents/${parentId}/notes/`;
  const params = [];
  if (startDate) params.push(`start_date=${startDate}`);
  if (endDate) params.push(`end_date=${endDate}`);
  if (params.length) url += '?' + params.join('&');
  return apiCall(url);
}

//===============================
// PARENT-CHILD LINKS
//===============================

export function createParentChildLink(parentId, childId, isMain = false) {
  return apiCall('/parent-child/', {
    method: 'POST',
    body: JSON.stringify({ parent_id: parentId, child_id: childId, is_main: isMain }),
  });
}

export function deleteParentChildLink(parentId, childId) {
  return apiCall(`/parent-child/${parentId}/${childId}`, {
    method: 'DELETE',
  });
}

export function getParentChildren(parentId) {
  return apiCall(`/parents/${parentId}/children/`);
}

export function getChildParents(childId) {
  return apiCall(`/children/${childId}/parents/`);
}

export function getParentChildrenWithRelations(parentId) {
  return apiCall(`/parents/${parentId}/children-relations/`);
}

export function updateParentChildLink(parentId, childId, isMain = false) {
  return apiCall(`/parent-child/${parentId}/${childId}`, {
    method: 'PATCH',
    body: JSON.stringify({ is_main: isMain }),
  });
}

//===============================
// LESSONS endpoints
//===============================

export function getLessons(skip = 0, limit = 100, startDate = null, endDate = null) {
  let url = `/lessons/?skip=${skip}&limit=${limit}`;
  if (startDate) url += `&start_date=${startDate}`;
  if (endDate) url += `&end_date=${endDate}`;
  return apiCall(url);
}

export function getLesson(lessonId) {
  return apiCall(`/lessons/${lessonId}`);
}

export function createLesson(data) {
  return apiCall('/lessons/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function updateLesson(lessonId, data) {
  return apiCall(`/lessons/${lessonId}/report`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function deleteLesson(lessonId) {
  return apiCall(`/lessons/${lessonId}`, {
    method: 'DELETE',
  });
}

export function getChildLessons(childId, startDate, endDate) {
  return apiCall(`/children/${childId}/lessons/?start_date=${startDate}&end_date=${endDate}`);
}

export function clearLessonNote(lessonId, field) {
  return apiCall(`/lessons/${lessonId}/clear-note/`, {
    method: 'PATCH',
    body: JSON.stringify({ field }),
  });
}

//===============================
// TARIFF endpoints
//===============================

export function getTariffs() {
  return apiCall('/tariff/');
}

export function getTariff(tariffId) {
  return apiCall(`/tariff/${tariffId}`);
}

export function createTariff(data) {
  return apiCall('/tariff/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function updateTariff(tariffId, data) {
  return apiCall(`/tariff/${tariffId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function deleteTariff(tariffId) {
  return apiCall(`/tariff/${tariffId}`, {
    method: 'DELETE',
  });
}

export function getArchivedTariffs() {
  return apiCall('/tariff/archived/');
}

//===============================
// CHILD-TARIFF-PERIODS endpoints
//===============================

export function assignTariff(childId, tariffId, startDate) {
  return apiCall(`/children/${childId}/assign-tariff/`, {
    method: 'POST',
    body: JSON.stringify({ tariff_id: tariffId, start_date: startDate }),
  });
}

export function updateTariffPeriod(tariffPeriodId, data) {
  return apiCall(`/tariff-periods/${tariffPeriodId}/`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function closeTariffPeriod(tariffPeriodId) {
  return apiCall(`/tariff-periods/${tariffPeriodId}/close/`, {
    method: 'POST',
  });
}

export function getChildTariffPeriods(childId) {
  return apiCall(`/children/${childId}/tariff-periods/`);
}

export function getChildrenWithTariffCount(tariffId) {
  return apiCall(`/tariff/${tariffId}/active-children-count/`)
}

//===============================
// PAYMENTS endpoints
//===============================

export function getPayments(skip = 0, limit = 100, startDate = null, endDate = null) {
  let url = `/payments/?skip=${skip}&limit=${limit}`;
  if (startDate) url += `&start_date=${startDate}`;
  if (endDate) url += `&end_date=${endDate}`;
  return apiCall(url);
}

export function getChildPayments(childId, startDate, endDate) {
  return apiCall(`/children/${childId}/payments/?start_date=${startDate}&end_date=${endDate}`);
}

export function createPayment(data) {
  return apiCall('/payments/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function deletePayment(paymentId) {
  return apiCall(`/payments/${paymentId}`, { method: 'DELETE' });
}

export function getParentPayments(parentId) {
  return apiCall(`/parents/${parentId}/payments/`);
}

export function getDebtors() {
  return apiCall('/debtors/');
}

export function getStudentStatus(childId) {
  return apiCall(`/children/${childId}/active-tariff/`);
}

export function getPaymentsSummary(startDate = null, endDate = null) {
  let url = '/stats/payments-summary/';
  const params = [];
  if (startDate) params.push(`start_date=${startDate}`);
  if (endDate)   params.push(`end_date=${endDate}`);
  if (params.length) url += '?' + params.join('&');
  return apiCall(url);
}

//===============================
// PAYMENT DETAILS endpoints
//===============================

export function getPaymentDetails(detailsId) {
  return apiCall(`/payment-details/${detailsId}`);
}

export function createPaymentDetails(data) {
  return apiCall('/payment-details/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function getLatestPaymentDetails() {
  return apiCall('/payment-details/latest/');
}

export function updatePaymentDetails(detailsId, data) {
  return apiCall(`/payment-details/${detailsId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

//===============================
// LESSON ATTACHMENTS endpoints
//===============================

export function getLessonAttachment(attachmentId) {
  return apiCall(`/lesson-attachments/${attachmentId}`);
}

export function createLessonAttachment(data) {
  return apiCall('/lesson-attachments/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}
