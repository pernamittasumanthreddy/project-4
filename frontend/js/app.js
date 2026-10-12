/**
 * HMS Member 4: Laboratory & Radiology Module Frontend Engine
 * Multi-Tenant SaaS LIS & RIS Application Logic
 */

const AppState = {
  currentTenant: 'metro-general',
  currentRole: 'LAB_TECHNICIAN',
  currentBranch: null,
  activeView: 'lab-dashboard',
  patients: [],
  categories: [],
  labTests: [],
  dicomEngine: null,
};

// API Client Wrapper with Multi-Tenant & RBAC headers
const API = {
  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      'X-Tenant-Code': AppState.currentTenant,
      'X-User-Role': AppState.currentRole,
      ...(options.headers || {})
    };

    try {
      const response = await fetch(endpoint, { ...options, headers });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Request failed with status ${response.status}`);
      }
      if (response.headers.get('content-type')?.includes('application/json')) {
        return await response.json();
      }
      return response;
    } catch (err) {
      Toast.show(err.message, 'danger');
      throw err;
    }
  },

  get(endpoint) { return this.request(endpoint, { method: 'GET' }); },
  post(endpoint, data) { return this.request(endpoint, { method: 'POST', body: JSON.stringify(data) }); },
  put(endpoint, data) { return this.request(endpoint, { method: 'PUT', body: JSON.stringify(data) }); },
  delete(endpoint) { return this.request(endpoint, { method: 'DELETE' }); }
};

// Toast notification shelf
const Toast = {
  show(message, type = 'success') {
    const shelf = document.getElementById('toastShelf');
    if (!shelf) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? '✓' : type === 'danger' ? '⚠' : 'ℹ';
    toast.innerHTML = `<span><b>${icon}</b> ${message}</span>`;
    shelf.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 200);
    }, 3500);
  }
};

// Application Router & View Dispatcher
async function switchView(viewName) {
  AppState.activeView = viewName;
  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.toggle('active', el.dataset.view === viewName);
  });

  const mainArea = document.getElementById('mainContentArea');
  mainArea.innerHTML = '<div style="padding: 40px; text-align: center; color: #64748b;">Loading workspace data...</div>';

  switch (viewName) {
    case 'lab-dashboard':
      await renderLabDashboard(mainArea);
      break;
    case 'lab-catalogue':
      await renderLabCatalogue(mainArea);
      break;
    case 'lab-orders':
      await renderLabOrders(mainArea);
      break;
    case 'lab-specimens':
      await renderLabSpecimens(mainArea);
      break;
    case 'lab-results':
      await renderLabResults(mainArea);
      break;
    case 'lab-reports':
      await renderLabReports(mainArea);
      break;
    case 'lab-critical':
      await renderLabCriticalAlerts(mainArea);
      break;
    case 'lab-analytics':
      await renderLabAnalytics(mainArea);
      break;
    case 'rad-dashboard':
      await renderRadDashboard(mainArea);
      break;
    case 'rad-orders':
      await renderRadOrders(mainArea);
      break;
    case 'rad-worklist':
      await renderRadWorklist(mainArea);
      break;
    case 'rad-viewer':
      await renderRadViewer(mainArea);
      break;
    case 'rad-reports':
      await renderRadReports(mainArea);
      break;
    case 'team-contracts':
      await renderTeamContracts(mainArea);
      break;
    default:
      await renderLabDashboard(mainArea);
  }
}

// 1. LABORATORY DASHBOARD VIEW
async function renderLabDashboard(container) {
  const data = await API.get('/api/laboratory/dashboard/');
  const stats = data.statistics;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Laboratory Executive Dashboard</h1>
        <p class="page-subtitle">Real-time specimen operations, diagnostic turnaround times & priority queues</p>
      </div>
      <div class="page-actions-group">
        <button class="btn btn-secondary btn-sm" onclick="switchView('lab-analytics')">📊 TAT Analytics</button>
        <button class="btn btn-primary btn-sm" onclick="openNewLabOrderModal()">+ New Lab Order</button>
      </div>
    </div>

    <!-- Live Calculated Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Orders Today</span>
          <span class="stat-icon">📋</span>
        </div>
        <div class="stat-value">${stats.total_orders_today}</div>
        <div class="stat-footer">Live persisted records for ${data.tenant_code}</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Awaiting Sample</span>
          <span class="stat-icon">🩸</span>
        </div>
        <div class="stat-value" style="color: #b45309;">${stats.orders_awaiting_collection}</div>
        <div class="stat-footer">Phlebotomy pending collection</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Samples In Lab</span>
          <span class="stat-icon">🔬</span>
        </div>
        <div class="stat-value" style="color: #0f766e;">${stats.samples_received_in_lab}</div>
        <div class="stat-footer">Received & Barcode Verified</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Results Awaiting Validation</span>
          <span class="stat-icon">⚖️</span>
        </div>
        <div class="stat-value" style="color: #6366f1;">${stats.results_awaiting_validation}</div>
        <div class="stat-footer">Entered by Technicians</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Reports Approved</span>
          <span class="stat-icon">✅</span>
        </div>
        <div class="stat-value" style="color: #16a34a;">${stats.approved_reports}</div>
        <div class="stat-footer">Signed by Consultant Pathologist</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Critical Alerts</span>
          <span class="stat-icon">🚨</span>
        </div>
        <div class="stat-value" style="color: #dc2626;">${stats.critical_alerts_unresolved}</div>
        <div class="stat-footer">Immediate Clinician Readback Required</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Rejected Samples</span>
          <span class="stat-icon">⚠️</span>
        </div>
        <div class="stat-value" style="color: #e11d48;">${stats.rejected_samples}</div>
        <div class="stat-footer">${stats.recollection_requests} Recollection Requests</div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Overdue Orders</span>
          <span class="stat-icon">⏱️</span>
        </div>
        <div class="stat-value" style="color: #7c2d12;">${stats.overdue_orders}</div>
        <div class="stat-footer">Exceeding TAT threshold</div>
      </div>
    </div>

    <!-- Priority Work Queues -->
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Recent Laboratory Orders Worklist</h3>
          <button class="btn btn-secondary btn-sm" onclick="switchView('lab-orders')">View All</button>
        </div>
        <div class="table-container" id="recentLabOrdersTable">
          <div style="padding: 20px; text-align: center; color: #64748b;">Loading priority worklist...</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Workload by Department</h3>
        </div>
        <div class="card-body">
          <div id="deptWorkloadList">
            ${data.categories.map(c => `
              <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; margin-bottom: 4px;">
                  <span>${c.name}</span>
                  <span style="color: #0f766e;">${c.order_count} tests</span>
                </div>
                <div style="height: 6px; background-color: #e2e8f0; border-radius: 999px; overflow: hidden;">
                  <div style="width: ${Math.min(100, (c.order_count + 1) * 20)}%; height: 100%; background-color: #0f766e;"></div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    </div>
  `;

  // Load table data for recent orders
  loadRecentLabOrdersSummary();
}

async function loadRecentLabOrdersSummary() {
  const container = document.getElementById('recentLabOrdersTable');
  if (!container) return;
  const res = await API.get('/api/laboratory/orders/?ordering=-ordered_at');
  const orders = res.results || res;

  if (!orders || orders.length === 0) {
    container.innerHTML = '<div style="padding: 20px; text-align: center; color: #64748b;">No laboratory orders in this tenant.</div>';
    return;
  }

  container.innerHTML = `
    <table class="clinical-table">
      <thead>
        <tr>
          <th>Accession / Order</th>
          <th>Patient</th>
          <th>Priority</th>
          <th>Tests Ordered</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        ${orders.slice(0, 5).map(o => `
          <tr>
            <td>
              <b>${o.accession_number}</b><br/>
              <span style="font-size: 11px; color: #64748b;">${o.order_number}</span>
            </td>
            <td>
              <b>${o.patient_details?.first_name} ${o.patient_details?.last_name}</b><br/>
              <span style="font-size: 11px; color: #64748b;">${o.patient_details?.uhid} (${o.patient_details?.gender})</span>
            </td>
            <td>
              <span class="badge ${o.priority === 'STAT' ? 'badge-critical' : o.priority === 'URGENT' ? 'badge-pending' : 'badge-ordered'}">
                ${o.priority}
              </span>
            </td>
            <td>${o.items?.map(i => i.test_details?.name).join(', ') || 'N/A'}</td>
            <td>
              <span class="badge badge-${o.status.toLowerCase()}">${o.status}</span>
            </td>
            <td>
              <button class="btn btn-secondary btn-sm" onclick="switchView('lab-results')">Open</button>
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

// 2. LABORATORY TEST CATALOGUE VIEW
async function renderLabCatalogue(container) {
  const [testsRes, catsRes] = await Promise.all([
    API.get('/api/laboratory/catalogue/'),
    API.get('/api/laboratory/categories/')
  ]);
  const tests = testsRes.results || testsRes;
  const categories = catsRes.results || catsRes;
  AppState.labTests = tests;
  AppState.categories = categories;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Laboratory Test Catalogue & Profiles</h1>
        <p class="page-subtitle">Configured LOINC parameters, specimen rules, reference ranges & critical alert thresholds</p>
      </div>
      <div class="page-actions-group">
        <button class="btn btn-primary btn-sm" onclick="openNewTestModal()">+ Add New Test Item</button>
      </div>
    </div>

    <div class="card">
      <div class="filter-bar">
        <input type="text" id="catalogueSearch" class="search-input" placeholder="Search test by name, LOINC, or code..." oninput="filterCatalogueTable(this.value)" />
        <select id="categoryFilter" class="form-control" style="max-width: 200px;" onchange="filterCatalogueByCategory(this.value)">
          <option value="">All Departments</option>
          ${categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('')}
        </select>
      </div>

      <div class="table-container">
        <table class="clinical-table" id="catalogueTable">
          <thead>
            <tr>
              <th>Code / LOINC</th>
              <th>Investigation Name</th>
              <th>Department</th>
              <th>Specimen & Container</th>
              <th>Reference Range</th>
              <th>Critical Limits</th>
              <th>Target TAT</th>
              <th>Charge</th>
            </tr>
          </thead>
          <tbody>
            ${tests.map(t => `
              <tr>
                <td>
                  <b>${t.test_code}</b><br/>
                  <span style="font-size: 11px; color: #0284c7;">LOINC: ${t.loinc_code || 'Pending'}</span>
                </td>
                <td><b>${t.name}</b></td>
                <td><span class="badge badge-ordered">${t.category_name}</span></td>
                <td>
                  <b>${t.specimen_type}</b><br/>
                  <span style="font-size: 11px; color: #64748b;">${t.container_type}</span>
                </td>
                <td>
                  ${t.ref_min !== null ? `${t.ref_min} - ${t.ref_max} ${t.unit}` : t.qualitative_normal}
                </td>
                <td>
                  ${t.critical_low !== null || t.critical_high !== null ? `
                    <span style="color: #dc2626; font-size: 11px; font-weight: 700;">
                      ${t.critical_low !== null ? `&lt; ${t.critical_low}` : ''}
                      ${t.critical_high !== null ? `| &gt; ${t.critical_high}` : ''}
                      ${t.unit}
                    </span>
                  ` : '<span style="color: #94a3b8; font-size: 11px;">None configured</span>'}
                </td>
                <td>⏱️ ${t.expected_tat_minutes} mins</td>
                <td><b>$${parseFloat(t.price).toFixed(2)}</b></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function filterCatalogueTable(query) {
  const q = query.toLowerCase();
  document.querySelectorAll('#catalogueTable tbody tr').forEach(row => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(q) ? '' : 'none';
  });
}

// 3. LABORATORY ORDERS & ACCESSIONING VIEW
async function renderLabOrders(container) {
  const res = await API.get('/api/laboratory/orders/');
  const orders = res.results || res;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Laboratory Orders & Accessioning Lifecycle</h1>
        <p class="page-subtitle">Physician orders intake, duplicate guards, accession assignment & barcode linking</p>
      </div>
      <div class="page-actions-group">
        <button class="btn btn-primary btn-sm" onclick="openNewLabOrderModal()">+ Create Investigation Order</button>
      </div>
    </div>

    <div class="card">
      <div class="filter-bar">
        <input type="text" class="search-input" placeholder="Search by Accession, Order #, Patient UHID..." oninput="filterOrdersTable(this.value)" />
        <select class="form-control" style="max-width: 180px;" onchange="filterOrdersByStatus(this.value)">
          <option value="">All Lifecycle States</option>
          <option value="SAMPLE_PENDING">Awaiting Collection</option>
          <option value="COLLECTED">Collected</option>
          <option value="RECEIVED_IN_LAB">Received in Lab</option>
          <option value="RESULTS_ENTERED">Results Entered</option>
          <option value="APPROVED">Approved</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <div class="table-container">
        <table class="clinical-table" id="ordersTable">
          <thead>
            <tr>
              <th>Accession #</th>
              <th>Order #</th>
              <th>Patient Details</th>
              <th>Ordering Doctor</th>
              <th>Priority</th>
              <th>Ordered Tests</th>
              <th>Specimens</th>
              <th>Lifecycle Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${orders.map(o => `
              <tr>
                <td><b>${o.accession_number}</b></td>
                <td><span style="font-size: 11px; font-family: monospace;">${o.order_number}</span></td>
                <td>
                  <b>${o.patient_details?.first_name} ${o.patient_details?.last_name}</b><br/>
                  <span style="font-size: 11px; color: #64748b;">${o.patient_details?.uhid} (${o.patient_details?.gender})</span>
                </td>
                <td>Dr. ${o.ordering_clinician}</td>
                <td>
                  <span class="badge ${o.priority === 'STAT' ? 'badge-critical' : o.priority === 'URGENT' ? 'badge-pending' : 'badge-ordered'}">
                    ${o.priority}
                  </span>
                </td>
                <td>
                  ${o.items?.map(i => `<span class="badge badge-ordered" style="margin: 2px;">${i.test_details?.name}</span>`).join('')}
                </td>
                <td>
                  ${o.specimens?.map(s => `
                    <div style="font-size: 11px;">
                      <b>${s.barcode_id}</b> (${s.specimen_type})
                    </div>
                  `).join('')}
                </td>
                <td>
                  <span class="badge badge-${o.status.toLowerCase()}">${o.status}</span>
                </td>
                <td>
                  <div style="display: flex; gap: 4px;">
                    <button class="btn btn-secondary btn-sm" onclick="viewOrderSpecimens('${o.id}')">Samples</button>
                    ${o.status !== 'APPROVED' && o.status !== 'CANCELLED' ? `
                      <button class="btn btn-danger btn-sm" onclick="cancelLabOrderPrompt('${o.id}')">Cancel</button>
                    ` : ''}
                  </div>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// 4. SPECIMEN MANAGEMENT & BARCODING VIEW
async function renderLabSpecimens(container) {
  const res = await API.get('/api/laboratory/specimens/');
  const specimens = res.results || res;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Specimen Management & Custody Tracking</h1>
        <p class="page-subtitle">Barcode generation, phlebotomy verification, intake acceptance & rejection recording</p>
      </div>
    </div>

    <div class="card">
      <div class="table-container">
        <table class="clinical-table">
          <thead>
            <tr>
              <th>Barcode Identifier</th>
              <th>Specimen Type</th>
              <th>Container Requirement</th>
              <th>Collection Status</th>
              <th>Collector Details</th>
              <th>Lab Storage Rack</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${specimens.map(s => `
              <tr>
                <td>
                  <b style="font-family: monospace; font-size: 13px;">${s.barcode_id}</b><br/>
                  <button class="btn btn-secondary btn-sm" style="margin-top: 4px; padding: 2px 6px; font-size: 10px;" onclick="printSpecimenLabelModal('${s.id}')">
                    🏷️ View / Print Label
                  </button>
                </td>
                <td><b>${s.specimen_type}</b></td>
                <td>${s.container_type}</td>
                <td>
                  <span class="badge badge-${s.status.toLowerCase()}">${s.status}</span>
                  ${s.recollection_needed ? '<br/><span class="badge badge-critical" style="margin-top: 2px;">Recollection Requested</span>' : ''}
                </td>
                <td>
                  ${s.collected_by ? `
                    <b>${s.collected_by}</b><br/>
                    <span style="font-size: 10px; color: #64748b;">${new Date(s.collected_at).toLocaleTimeString()}</span>
                  ` : '<span style="color: #94a3b8;">Not collected</span>'}
                </td>
                <td>${s.storage_rack || 'Pending Intake'}</td>
                <td>
                  <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                    ${s.status === 'PENDING' ? `
                      <button class="btn btn-primary btn-sm" onclick="collectSampleAction('${s.id}')">Collect Sample</button>
                    ` : ''}
                    ${s.status === 'COLLECTED' ? `
                      <button class="btn btn-success btn-sm" onclick="receiveInLabAction('${s.id}')">Receive in Lab</button>
                    ` : ''}
                    ${s.status !== 'REJECTED' ? `
                      <button class="btn btn-danger btn-sm" onclick="rejectSamplePrompt('${s.id}')">Reject Sample</button>
                    ` : `
                      <span style="font-size: 11px; color: #dc2626; font-weight: 600;">Reason: ${s.rejection_reason}</span>
                    `}
                  </div>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// 5. RESULT ENTRY & VALIDATION VIEW
async function renderLabResults(container) {
  const res = await API.get('/api/laboratory/results/');
  const results = res.results || res;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Diagnostic Result Entry & Pathologist Sign-Off</h1>
        <p class="page-subtitle">Technician numeric entry, automatic abnormal & critical limit flags, supervisor validation & pathologist approval</p>
      </div>
    </div>

    <div class="card">
      <div class="table-container">
        <table class="clinical-table">
          <thead>
            <tr>
              <th>Investigation / LOINC</th>
              <th>Observed Result</th>
              <th>Units</th>
              <th>Reference Range</th>
              <th>Evaluation Flag</th>
              <th>Entry & Review State</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${results.map(r => `
              <tr>
                <td>
                  <b>${r.test_name}</b><br/>
                  <span style="font-size: 11px; color: #64748b;">[${r.test_code}] LOINC: ${r.loinc_code || '-'}</span>
                </td>
                <td>
                  <b style="font-size: 14px;">
                    ${r.numeric_value !== null ? r.numeric_value : (r.text_value || '<span style="color:#94a3b8;">Pending Entry</span>')}
                  </b>
                  ${r.technician_notes ? `<br/><span style="font-size: 10px; color: #64748b;">Note: ${r.technician_notes}</span>` : ''}
                </td>
                <td>${r.unit || '-'}</td>
                <td>${r.ref_range_display}</td>
                <td>
                  <span class="${r.is_critical ? 'flag-critical badge badge-critical' : r.is_abnormal ? 'flag-abnormal' : 'flag-normal'}">
                    ${r.flag}
                  </span>
                </td>
                <td>
                  <span class="badge badge-${r.status.toLowerCase()}">${r.status}</span><br/>
                  ${r.entered_by ? `<span style="font-size: 10px; color: #64748b;">By: ${r.entered_by}</span>` : ''}
                </td>
                <td>
                  <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                    <button class="btn btn-secondary btn-sm" onclick="openEnterResultModal('${r.id}', '${r.test_name}', '${r.unit}', '${r.numeric_value || ''}')">
                      📝 Enter / Edit
                    </button>
                    ${r.status === 'ENTERED' ? `
                      <button class="btn btn-primary btn-sm" onclick="validateResultAction('${r.id}')">Validate</button>
                    ` : ''}
                    ${r.status === 'VALIDATED' ? `
                      <button class="btn btn-success btn-sm" onclick="approveResultAction('${r.id}')">Pathologist Sign-Off</button>
                    ` : ''}
                    ${r.status === 'APPROVED' ? `
                      <button class="btn btn-danger btn-sm" onclick="amendResultModal('${r.id}', '${r.test_name}')">Amend</button>
                    ` : ''}
                  </div>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// 6. DIAGNOSTIC REPORTS & PDF VIEW
async function renderLabReports(container) {
  const res = await API.get('/api/laboratory/reports/');
  const reports = res.results || res;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Final Laboratory Diagnostic Reports</h1>
        <p class="page-subtitle">Accredited diagnostic reports, cryptographically signed by consultant pathologists, with secure PDF streaming</p>
      </div>
    </div>

    <div class="card">
      <div class="table-container">
        <table class="clinical-table">
          <thead>
            <tr>
              <th>Report Number</th>
              <th>Accession</th>
              <th>Patient Name</th>
              <th>Version</th>
              <th>Approved Signatory</th>
              <th>Finalized Timestamp</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            ${reports.map(rep => `
              <tr>
                <td><b>${rep.report_number}</b></td>
                <td>${rep.accession_number}</td>
                <td><b>${rep.patient_name}</b></td>
                <td>v${rep.version} ${rep.is_amended ? '<span class="badge badge-warning">AMENDED</span>' : ''}</td>
                <td>${rep.approved_by}</td>
                <td>${new Date(rep.approved_at).toLocaleString()}</td>
                <td>
                  <a href="/api/laboratory/reports/${rep.id}/download_pdf/" target="_blank" class="btn btn-primary btn-sm">
                    📄 Download / View PDF
                  </a>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// 7. CRITICAL RESULTS ALERT CENTER
async function renderLabCriticalAlerts(container) {
  const res = await API.get('/api/laboratory/critical-alerts/');
  const alerts = res.results || res;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Critical Laboratory Values Escalation Center</h1>
        <p class="page-subtitle">Life-threatening laboratory measurements requiring immediate documented clinician readback verification</p>
      </div>
    </div>

    <div class="card">
      <div class="table-container">
        <table class="clinical-table">
          <thead>
            <tr>
              <th>Alert Status</th>
              <th>Patient</th>
              <th>Investigation & Value</th>
              <th>Clinician Responsible</th>
              <th>Triggered Time</th>
              <th>Telephone Readback Call Log</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            ${alerts.map(a => `
              <tr>
                <td>
                  <span class="badge ${a.alert_status === 'ACKNOWLEDGED' ? 'badge-approved' : 'badge-critical'}">
                    ${a.alert_status}
                  </span>
                </td>
                <td><b>${a.patient_name}</b></td>
                <td>
                  <b style="color: #dc2626;">${a.test_name}</b><br/>
                  <span style="font-weight: 700; font-size: 13px;">Observed: ${a.observed_value}</span>
                </td>
                <td>Dr. ${a.clinician_name}</td>
                <td>${new Date(a.triggered_at).toLocaleTimeString()}</td>
                <td>
                  <span style="font-size: 11px; color: #475569;">${a.call_log_notes || 'Pending readback verification'}</span>
                </td>
                <td>
                  ${a.alert_status !== 'ACKNOWLEDGED' ? `
                    <button class="btn btn-success btn-sm" onclick="acknowledgeCriticalAlertPrompt('${a.id}', '${a.clinician_name}')">
                      📞 Document Readback
                    </button>
                  ` : '<span style="color: #16a34a; font-weight: 600;">✓ Acknowledged</span>'}
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// 8. TURNAROUND TIME ANALYTICS
async function renderLabAnalytics(container) {
  const res = await API.get('/api/laboratory/tat-analytics/');

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Turnaround Time (TAT) & Quality Control Analytics</h1>
        <p class="page-subtitle">Specimen rejection rate, priority processing benchmarks and audit CSV export</p>
      </div>
      <div class="page-actions-group">
        <a href="/api/laboratory/tat-analytics/?export=csv" class="btn btn-secondary btn-sm">📥 Export CSV Audit Report</a>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Target Processing TAT</span><span>🎯</span></div>
        <div class="stat-value">${res.average_target_tat_minutes} min</div>
        <div class="stat-footer">Benchmark for Routine Orders</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Specimen Rejection Rate</span><span>⚠️</span></div>
        <div class="stat-value" style="color: #dc2626;">${res.rejection_rate_percent}%</div>
        <div class="stat-footer">${res.rejected_specimens} of ${res.total_specimens} collected</div>
      </div>
    </div>
  `;
}

// 9. RADIOLOGY DASHBOARD
async function renderRadDashboard(container) {
  const data = await API.get('/api/radiology/dashboard/');
  const stats = data.statistics;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Radiology Information System (RIS) Dashboard</h1>
        <p class="page-subtitle">Modality equipment suites, DICOM Modality Worklists (MWL) & PACS interpretation</p>
      </div>
      <div class="page-actions-group">
        <button class="btn btn-secondary btn-sm" onclick="switchView('rad-worklist')">📋 Modality Worklist</button>
        <button class="btn btn-primary btn-sm" onclick="switchView('rad-viewer')">🖥️ Open Medical DICOM Viewer</button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Radiology Orders Today</span><span>🩻</span></div>
        <div class="stat-value">${stats.total_orders_today}</div>
        <div class="stat-footer">Persisted in ${data.tenant_code}</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Scheduled Procedures</span><span>📅</span></div>
        <div class="stat-value" style="color: #0369a1;">${stats.scheduled}</div>
        <div class="stat-footer">In Modality Slots</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Scans In Progress</span><span>⚡</span></div>
        <div class="stat-value" style="color: #b45309;">${stats.scans_in_progress}</div>
        <div class="stat-footer">Acquiring Projections/Slices</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Awaiting Radiologist</span><span>👁️</span></div>
        <div class="stat-value" style="color: #7c3aed;">${stats.awaiting_interpretation}</div>
        <div class="stat-footer">Studies Stored in PACS</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Finalized Reports</span><span>✅</span></div>
        <div class="stat-value" style="color: #16a34a;">${stats.approved_reports}</div>
        <div class="stat-footer">Signed with Recommendations</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Imaging Modality Equipment Status</h3>
      </div>
      <div class="card-body">
        <div class="table-container">
          <table class="clinical-table">
            <thead>
              <tr>
                <th>Modality Name</th>
                <th>Type</th>
                <th>Room Suite</th>
                <th>Active Orders</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              ${data.modalities.map(m => `
                <tr>
                  <td><b>${m.name}</b></td>
                  <td><span class="badge badge-ordered">${m.modality_type}</span></td>
                  <td>${m.room_number}</td>
                  <td><b>${m.active_orders}</b> exams</td>
                  <td>
                    <button class="btn btn-secondary btn-sm" onclick="switchView('rad-worklist')">View Worklist</button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

// 10. RADIOLOGY ORDERS
async function renderRadOrders(container) {
  const res = await API.get('/api/radiology/orders/');
  const orders = res.results || res;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Radiology Orders & Examination Worklist</h1>
        <p class="page-subtitle">Modality scheduling, patient arrival check-in, technologist acquisition & study storage</p>
      </div>
      <div class="page-actions-group">
        <button class="btn btn-primary btn-sm" onclick="openNewRadOrderModal()">+ Create Imaging Order</button>
      </div>
    </div>

    <div class="card">
      <div class="table-container">
        <table class="clinical-table">
          <thead>
            <tr>
              <th>Accession #</th>
              <th>Order #</th>
              <th>Patient</th>
              <th>Procedure Requested</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${orders.map(o => `
              <tr>
                <td><b>${o.accession_number}</b></td>
                <td><span style="font-size: 11px; font-family: monospace;">${o.order_number}</span></td>
                <td>
                  <b>${o.patient_details?.first_name} ${o.patient_details?.last_name}</b><br/>
                  <span style="font-size: 11px; color: #64748b;">${o.patient_details?.uhid}</span>
                </td>
                <td>${o.items?.map(i => i.procedure_details?.name).join(', ') || 'N/A'}</td>
                <td><span class="badge badge-ordered">${o.priority}</span></td>
                <td><span class="badge badge-${o.status.toLowerCase()}">${o.status}</span></td>
                <td>
                  <div style="display: flex; gap: 4px;">
                    ${o.status === 'ORDERED' ? `
                      <button class="btn btn-secondary btn-sm" onclick="scheduleRadOrderAction('${o.id}')">Schedule</button>
                    ` : ''}
                    ${o.status === 'SCHEDULED' ? `
                      <button class="btn btn-secondary btn-sm" onclick="markPatientArrivedAction('${o.id}')">Mark Arrived</button>
                    ` : ''}
                    ${o.status === 'ARRIVED' ? `
                      <button class="btn btn-primary btn-sm" onclick="startScanAction('${o.id}')">Start Scan</button>
                    ` : ''}
                    ${o.status === 'IN_PROGRESS' ? `
                      <button class="btn btn-success btn-sm" onclick="completeScanAction('${o.id}')">Complete Acquisition</button>
                    ` : ''}
                    ${o.status === 'REPORT_PENDING' || o.status === 'APPROVED' ? `
                      <button class="btn btn-secondary btn-sm" onclick="switchView('rad-viewer')">View in DICOM</button>
                    ` : ''}
                  </div>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// 11. DICOM MODALITY WORKLIST (MWL)
async function renderRadWorklist(container) {
  const res = await API.get('/api/radiology/worklist/');
  const worklist = res.worklist || [];

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">DICOM Modality Worklist (MWL) Interface</h1>
        <p class="page-subtitle">DICOM PS3.4 Scheduled Procedure Step (SPS) worklist query feeds for modality scanners</p>
      </div>
    </div>

    <div class="card">
      <div class="table-container">
        <table class="clinical-table">
          <thead>
            <tr>
              <th>Accession (0008,0050)</th>
              <th>Patient ID (0010,0020)</th>
              <th>Patient Name (0010,0010)</th>
              <th>Modality (0008,0060)</th>
              <th>Station AE Title (0040,0001)</th>
              <th>Scheduled Procedure (0040,0007)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${worklist.map(w => `
              <tr>
                <td><b>${w.accession_number}</b></td>
                <td>${w.patient_id}</td>
                <td><b>${w.patient_name}</b></td>
                <td><span class="badge badge-ordered">${w.modality}</span></td>
                <td><code>${w.scheduled_station_ae}</code></td>
                <td>${w.scheduled_procedure_description}</td>
                <td><span class="badge badge-pending">${w.status}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// 12. MEDICAL IMAGE & DICOM VIEWER WORKSTATION
async function renderRadViewer(container) {
  const res = await API.get('/api/radiology/studies/');
  const studies = res.results || res;

  container.innerHTML = `
    <div class="page-header-row" style="margin-bottom: 12px;">
      <div>
        <h1 class="page-title">Diagnostic Medical DICOM Viewer Workstation</h1>
        <p class="page-subtitle">Standard DICOMweb PS3.18 parser, multi-slice stack rendering, caliper tools & clinical window presets</p>
      </div>
    </div>

    <div class="dicom-workstation">
      <!-- Left Studies & Series Panel -->
      <div class="dicom-sidebar">
        <div class="dicom-sidebar-header">PACS DICOM Studies (${studies.length})</div>
        <div class="dicom-series-list">
          ${studies.map((s, idx) => `
            <div class="series-thumbnail-card ${idx === 0 ? 'active' : ''}" onclick="selectStudyInViewer('${s.id}')" data-study-id="${s.id}">
              <img src="/api/dicomweb/studies/${s.study_instance_uid}/series/${s.study_instance_uid}.1/instances/${s.study_instance_uid}.1.1/rendered" class="series-thumb-img" alt="DICOM Preview" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'100\\' height=\\'100\\'><rect fill=\\'%23222\\' width=\\'100\\' height=\\'100\\'/></svg>'" />
              <div class="series-meta-title">${s.study_description}</div>
              <div class="series-meta-sub">${s.modality_type} | Acc: ${s.accession_number}</div>
              <div class="series-meta-sub">${s.patient_details?.first_name} ${s.patient_details?.last_name}</div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Main Interactive Viewport -->
      <div class="dicom-viewport-area">
        <div class="dicom-toolbar">
          <button class="tool-btn active" data-tool="wl" onclick="setViewerTool('wl')">☀️ Window/Level</button>
          <button class="tool-btn" data-tool="pan" onclick="setViewerTool('pan')">✋ Pan</button>
          <button class="tool-btn" data-tool="zoom" onclick="setViewerTool('zoom')">🔍 Zoom</button>
          <button class="tool-btn" data-tool="caliper" onclick="setViewerTool('caliper')">📏 Caliper (mm)</button>
          <button class="tool-btn" onclick="toggleViewerInvert()">🌓 Invert</button>
          <button class="tool-btn" onclick="resetViewerViewport()">🔄 Reset</button>

          <div style="border-left: 1px solid #374151; height: 24px; margin: 0 4px;"></div>
          
          <span style="font-size: 11px; color: #9ca3af;">Presets:</span>
          <button class="tool-btn" onclick="setViewerPreset('soft_tissue')">Soft Tissue</button>
          <button class="tool-btn" onclick="setViewerPreset('bone')">Bone</button>
          <button class="tool-btn" onclick="setViewerPreset('lung')">Lung</button>
          <button class="tool-btn" onclick="setViewerPreset('brain')">Brain</button>

          <div style="margin-left: auto;">
            <button class="tool-btn" onclick="openDicomHeaderModal()">ℹ️ DICOM Tags</button>
          </div>
        </div>

        <div class="canvas-viewport">
          <canvas id="dicomCanvas"></canvas>
          <div id="hudTopLeft" class="dicom-hud-tl"></div>
          <div id="hudTopRight" class="dicom-hud-tr"></div>
          <div id="hudBottomLeft" class="dicom-hud-bl"></div>
          <div id="hudBottomRight" class="dicom-hud-br"></div>
        </div>
      </div>
    </div>
  `;

  // Initialize DICOM Engine
  AppState.dicomEngine = new DicomViewerEngine('dicomCanvas');
  if (studies.length > 0) {
    AppState.dicomEngine.loadStudy(studies[0]);
    AppState.activeStudyData = studies[0];
  }
}

function selectStudyInViewer(studyId) {
  API.get(`/api/radiology/studies/${studyId}/`).then(study => {
    AppState.activeStudyData = study;
    document.querySelectorAll('.series-thumbnail-card').forEach(c => {
      c.classList.toggle('active', c.dataset.studyId === studyId);
    });
    AppState.dicomEngine.loadStudy(study);
  });
}

function setViewerTool(tool) { AppState.dicomEngine?.setTool(tool); }
function setViewerPreset(p) { AppState.dicomEngine?.setPreset(p); }
function toggleViewerInvert() { AppState.dicomEngine?.toggleInvert(); }
function resetViewerViewport() { AppState.dicomEngine?.resetViewport(); }

// 13. RADIOLOGY REPORTING WORKSTATION
async function renderRadReports(container) {
  const res = await API.get('/api/radiology/reports/');
  const reports = res.results || res;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">Radiology Diagnostic Reporting Workstation</h1>
        <p class="page-subtitle">Structured findings, clinical impressions, recommendations, consultant sign-offs & PDF generation</p>
      </div>
    </div>

    <div class="card">
      <div class="table-container">
        <table class="clinical-table">
          <thead>
            <tr>
              <th>Report Number</th>
              <th>Study Description</th>
              <th>Patient</th>
              <th>Version / Status</th>
              <th>Interpreting Radiologist</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${reports.map(r => `
              <tr>
                <td><b>${r.report_number}</b></td>
                <td>${r.study_description}</td>
                <td><b>${r.patient_name}</b></td>
                <td>
                  <span class="badge badge-${r.status.toLowerCase()}">${r.status}</span>
                  v${r.version}
                </td>
                <td>${r.reporting_radiologist}</td>
                <td>
                  <div style="display: flex; gap: 4px;">
                    <button class="btn btn-secondary btn-sm" onclick="openEditRadReportModal('${r.id}')">📝 Edit Findings</button>
                    ${r.status === 'APPROVED' ? `
                      <a href="/api/radiology/reports/${r.id}/download_pdf/" target="_blank" class="btn btn-primary btn-sm">📄 Download PDF</a>
                      <button class="btn btn-danger btn-sm" onclick="amendRadReportModal('${r.id}')">Amend</button>
                    ` : `
                      <button class="btn btn-success btn-sm" onclick="approveRadReportAction('${r.id}')">Sign & Finalize</button>
                    `}
                  </div>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// 14. TEAM INTEGRATION HUB
async function renderTeamContracts(container) {
  const res = await API.get('/api/contracts/summary/');
  const billingRes = await API.get('/api/contracts/billing-events/');
  const billingEvents = billingRes.results || billingRes;

  container.innerHTML = `
    <div class="page-header-row">
      <div>
        <h1 class="page-title">HMS Team Integration Hub (Members 1, 2, 3, 6)</h1>
        <p class="page-subtitle">Live interface contracts, data models exchanged, multi-tenant headers & billable charge events</p>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Member 1: Tenant & Auth</span><span>🏢</span></div>
        <div class="stat-value" style="font-size: 18px; color: #0f766e;">${res.contracts_status.member_1_auth_tenant}</div>
        <div class="stat-footer">Active Tenant: ${res.active_tenant?.name}</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Member 2: Patient Registry</span><span>👤</span></div>
        <div class="stat-value" style="font-size: 20px; color: #0369a1;">${res.contracts_status.member_2_patients}</div>
        <div class="stat-footer">Demographic contract synced</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Member 3: Clinical Encounters</span><span>🩺</span></div>
        <div class="stat-value" style="font-size: 20px; color: #6366f1;">${res.contracts_status.member_3_clinical}</div>
        <div class="stat-footer">Doctor consultations linked</div>
      </div>
      <div class="stat-card">
        <div class="stat-header"><span class="stat-title">Member 6: Chargeable Events</span><span>💳</span></div>
        <div class="stat-value" style="font-size: 20px; color: #16a34a;">${res.contracts_status.member_6_billing}</div>
        <div class="stat-footer">Events emitted to billing</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Emitted Chargeable Events for Member 6 (Billing & Insurance)</h3>
      </div>
      <div class="table-container">
        <table class="clinical-table">
          <thead>
            <tr>
              <th>Module</th>
              <th>Order ID</th>
              <th>Service Code</th>
              <th>Service Description</th>
              <th>Amount ($)</th>
              <th>Status</th>
              <th>Emitted Time</th>
            </tr>
          </thead>
          <tbody>
            ${billingEvents.map(b => `
              <tr>
                <td><span class="badge ${b.module === 'LIS' ? 'badge-received' : 'badge-processing'}">${b.module}</span></td>
                <td><b>${b.order_id}</b></td>
                <td><code>${b.service_code}</code></td>
                <td>${b.service_name}</td>
                <td><b>$${parseFloat(b.amount).toFixed(2)}</b></td>
                <td><span class="badge badge-approved">${b.status}</span></td>
                <td>${new Date(b.emitted_at).toLocaleString()}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// ----------------- MODAL ACTIONS & EVENT HANDLERS ----------------- //

async function openNewLabOrderModal() {
  const [patientsRes, testsRes] = await Promise.all([
    API.get('/api/contracts/patients/'),
    API.get('/api/laboratory/catalogue/')
  ]);
  const patients = patientsRes.results || patientsRes;
  const tests = testsRes.results || testsRes;

  showModal('Create Laboratory Order', `
    <form id="newLabOrderForm" onsubmit="submitNewLabOrder(event)">
      <div class="form-group">
        <label class="form-label">Select Patient (Member 2 Registry)</label>
        <select id="orderPatientId" class="form-control" required>
          ${patients.map(p => `<option value="${p.id}">${p.full_name} (${p.uhid}) - DOB: ${p.dob}</option>`).join('')}
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Ordering Physician</label>
        <input type="text" id="orderDoctor" class="form-control" value="Dr. Elena Rostova, MD" required />
      </div>

      <div class="form-group">
        <label class="form-label">Priority</label>
        <select id="orderPriority" class="form-control">
          <option value="ROUTINE">Routine (Standard TAT)</option>
          <option value="URGENT">Urgent (Priority Processing)</option>
          <option value="STAT">STAT (Immediate Emergency Analysis)</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Select Laboratory Tests</label>
        <div style="max-height: 140px; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px;">
          ${tests.map(t => `
            <label style="display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 6px;">
              <input type="checkbox" name="labTests" value="${t.id}" />
              <span><b>${t.name}</b> (${t.category_name}) - $${t.price}</span>
            </label>
          `).join('')}
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Clinical Indication / Symptoms</label>
        <textarea id="orderClinical" class="form-control" rows="2" placeholder="Clinical justification..."></textarea>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
        <button type="submit" class="btn btn-primary">Submit Investigation Order</button>
      </div>
    </form>
  `);
}

async function submitNewLabOrder(e) {
  e.preventDefault();
  const patient_id = document.getElementById('orderPatientId').value;
  const ordering_clinician = document.getElementById('orderDoctor').value;
  const priority = document.getElementById('orderPriority').value;
  const clinical_indications = document.getElementById('orderClinical').value;
  const test_ids = Array.from(document.querySelectorAll('input[name="labTests"]:checked')).map(cb => cb.value);

  if (test_ids.length === 0) {
    Toast.show('Please select at least one laboratory test.', 'warning');
    return;
  }

  await API.post('/api/laboratory/orders/', {
    patient_id, ordering_clinician, priority, clinical_indications, test_ids
  });
  Toast.show('Laboratory order placed and accession number generated!');
  closeModal();
  switchView('lab-orders');
}

async function collectSampleAction(specimenId) {
  await API.post(`/api/laboratory/specimens/${specimenId}/collect_sample/`, {
    collected_by: 'Senior Phlebotomist'
  });
  Toast.show('Specimen collected successfully!');
  switchView('lab-specimens');
}

async function receiveInLabAction(specimenId) {
  await API.post(`/api/laboratory/specimens/${specimenId}/receive_in_lab/`, {
    received_by: 'Lab Intake Technologist',
    storage_rack: 'Accession Cold Rack A-02'
  });
  Toast.show('Specimen received and verified in laboratory!');
  switchView('lab-specimens');
}

function rejectSamplePrompt(specimenId) {
  showModal('Reject Compromised Specimen', `
    <div class="form-group">
      <label class="form-label">Rejection Reason</label>
      <select id="rejectReason" class="form-control">
        <option value="Hemolyzed Specimen">Hemolyzed Specimen</option>
        <option value="Clotted Blood (EDTA)">Clotted Blood (EDTA)</option>
        <option value="Insufficient Specimen Volume (QNS)">Insufficient Specimen Volume (QNS)</option>
        <option value="Mislabeled Specimen Container">Mislabeled Specimen Container</option>
        <option value="Inappropriate Specimen Container">Inappropriate Specimen Container</option>
      </select>
    </div>
    <div class="form-group">
      <label class="form-label">Quality Documentation Notes</label>
      <textarea id="rejectNotes" class="form-control" rows="2" placeholder="Document rejection observations..."></textarea>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-danger" onclick="submitSampleRejection('${specimenId}')">Confirm Rejection</button>
    </div>
  `);
}

async function submitSampleRejection(specimenId) {
  const reason = document.getElementById('rejectReason').value;
  const notes = document.getElementById('rejectNotes').value;
  await API.post(`/api/laboratory/specimens/${specimenId}/reject_sample/`, {
    reason, notes, actor_name: 'Lab QA Supervisor'
  });
  Toast.show('Specimen rejected. Recollection request emitted.', 'warning');
  closeModal();
  switchView('lab-specimens');
}

async function printSpecimenLabelModal(specimenId) {
  const res = await API.get(`/api/laboratory/specimens/${specimenId}/label_data/`);
  showModal('Printable Specimen Barcode Label', `
    <div style="background-color: #fff; border: 2px dashed #94a3b8; padding: 16px; border-radius: 8px; text-align: center;">
      <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px;">${res.patient_name}</div>
      <div style="font-size: 12px; color: #475569;">MRN: <b>${res.patient_uhid}</b> | ${res.dob_gender}</div>
      <div style="margin: 12px 0;">
        ${res.svg_barcode}
      </div>
      <div style="font-family: monospace; font-size: 14px; font-weight: 700;">${res.barcode_id}</div>
      <div style="font-size: 11px; margin-top: 6px; color: #64748b;">
        Acc: ${res.accession_number} | Tube: ${res.container_type} | ${res.priority}
      </div>
    </div>
    <div class="modal-footer" style="margin-top: 16px;">
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
      <button class="btn btn-primary" onclick="window.print()">🖨️ Print Label</button>
    </div>
  `);
}

function openEnterResultModal(resultId, testName, unit, currentVal) {
  showModal(`Enter Result: ${testName}`, `
    <div class="form-group">
      <label class="form-label">Observed Measurement Value (${unit || 'Unit'})</label>
      <input type="number" step="0.01" id="resNumericVal" class="form-control" value="${currentVal}" placeholder="e.g. 14.5" />
    </div>
    <div class="form-group">
      <label class="form-label">Qualitative / Text Finding (Optional)</label>
      <input type="text" id="resTextVal" class="form-control" placeholder="e.g. Negative, Non-Reactive" />
    </div>
    <div class="form-group">
      <label class="form-label">Technician Observations</label>
      <input type="text" id="resTechNotes" class="form-control" placeholder="Analyzer run #, Delta check..." />
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="submitResultEntry('${resultId}')">Record Value</button>
    </div>
  `);
}

async function submitResultEntry(resultId) {
  const numeric_value = document.getElementById('resNumericVal').value;
  const text_value = document.getElementById('resTextVal').value;
  const technician_notes = document.getElementById('resTechNotes').value;

  const res = await API.post(`/api/laboratory/results/${resultId}/enter_result/`, {
    numeric_value, text_value, technician_notes, entered_by: 'Senior Medical Technologist'
  });
  if (res.is_critical) {
    Toast.show(`CRITICAL ALERT: Result triggered ${res.flag}!`, 'danger');
  } else {
    Toast.show(`Result saved (${res.flag})`);
  }
  closeModal();
  switchView('lab-results');
}

async function validateResultAction(resultId) {
  await API.post(`/api/laboratory/results/${resultId}/validate_result/`, {
    validated_by: 'Supervisor Biochemist'
  });
  Toast.show('Result validated by supervisor!');
  switchView('lab-results');
}

async function approveResultAction(resultId) {
  await API.post(`/api/laboratory/results/${resultId}/approve_result/`, {
    approved_by: 'Dr. Sarah Al-Mansoor, MD (Pathologist)'
  });
  Toast.show('Result digitally approved & signed! Report generated.');
  switchView('lab-results');
}

function amendResultModal(resultId, testName) {
  showModal(`Clinical Amendment: ${testName}`, `
    <div class="form-group">
      <label class="form-label">Corrected Numeric Value</label>
      <input type="number" step="0.01" id="amendNumeric" class="form-control" required />
    </div>
    <div class="form-group">
      <label class="form-label">Mandatory Clinical Amendment Reason</label>
      <textarea id="amendReason" class="form-control" rows="2" placeholder="Document justification for correction..." required></textarea>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-danger" onclick="submitResultAmendment('${resultId}')">Save Amended Version</button>
    </div>
  `);
}

async function submitResultAmendment(resultId) {
  const numeric_value = document.getElementById('amendNumeric').value;
  const reason = document.getElementById('amendReason').value;
  if (!reason) {
    Toast.show('Amendment reason is required.', 'warning');
    return;
  }
  await API.post(`/api/laboratory/results/${resultId}/amend_result/`, {
    numeric_value, reason, amended_by: 'Pathology Director'
  });
  Toast.show('Result amended and historical version snapshot created.');
  closeModal();
  switchView('lab-results');
}

function acknowledgeCriticalAlertPrompt(alertId, doctorName) {
  showModal('Document Critical Value Telephone Readback', `
    <div class="form-group">
      <label class="form-label">Doctor Acknowledging</label>
      <input type="text" id="ackDoctor" class="form-control" value="Dr. ${doctorName}" required />
    </div>
    <div class="form-group">
      <label class="form-label">Readback Verification Call Log</label>
      <textarea id="ackNotes" class="form-control" rows="2">Direct telephone readback verified with attending physician.</textarea>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-success" onclick="submitCriticalAck('${alertId}')">Verify & Close Alert</button>
    </div>
  `);
}

async function submitCriticalAck(alertId) {
  const acknowledged_by = document.getElementById('ackDoctor').value;
  const call_log_notes = document.getElementById('ackNotes').value;
  await API.post(`/api/laboratory/critical-alerts/${alertId}/acknowledge/`, {
    acknowledged_by, call_log_notes
  });
  Toast.show('Critical alert telephone readback documented.');
  closeModal();
  switchView('lab-critical');
}

// Radiology Modality Actions
async function startScanAction(orderId) {
  await API.post(`/api/radiology/orders/${orderId}/start_scan/`);
  Toast.show('Scan acquisition started!');
  switchView('rad-orders');
}

async function completeScanAction(orderId) {
  await API.post(`/api/radiology/orders/${orderId}/complete_scan/`, {
    technologist: 'Senior Radiologic Technologist'
  });
  Toast.show('Scan completed! DICOM dataset generated & stored in PACS.');
  switchView('rad-orders');
}

async function approveRadReportAction(reportId) {
  await API.post(`/api/radiology/reports/${reportId}/approve_report/`, {
    approved_by: 'Dr. Arthur Sterling, MD (Consultant Radiologist)'
  });
  Toast.show('Radiology interpretation signed off & released!');
  switchView('rad-reports');
}

function openDicomHeaderModal() {
  const study = AppState.activeStudyData;
  if (!study) return;
  showModal('DICOM PS3.10 Header Metadata Inspector', `
    <div style="max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 11px;">
      <table class="clinical-table">
        <thead>
          <tr><th>Tag (Group, Element)</th><th>VR</th><th>Attribute Name</th><th>Value</th></tr>
        </thead>
        <tbody>
          <tr><td>(0020,000D)</td><td>UI</td><td>Study Instance UID</td><td>${study.study_instance_uid}</td></tr>
          <tr><td>(0008,0050)</td><td>SH</td><td>Accession Number</td><td>${study.accession_number}</td></tr>
          <tr><td>(0008,0060)</td><td>CS</td><td>Modality</td><td>${study.modality_type}</td></tr>
          <tr><td>(0008,1030)</td><td>LO</td><td>Study Description</td><td>${study.study_description}</td></tr>
          <tr><td>(0010,0010)</td><td>PN</td><td>Patient Name</td><td>${study.patient_details?.last_name}^${study.patient_details?.first_name}</td></tr>
          <tr><td>(0010,0020)</td><td>LO</td><td>Patient ID (UHID)</td><td>${study.patient_details?.uhid}</td></tr>
          <tr><td>(0028,0010)</td><td>US</td><td>Rows</td><td>512</td></tr>
          <tr><td>(0028,0011)</td><td>US</td><td>Columns</td><td>512</td></tr>
          <tr><td>(0028,0100)</td><td>US</td><td>Bits Allocated</td><td>16</td></tr>
          <tr><td>(0028,0101)</td><td>US</td><td>Bits Stored</td><td>12</td></tr>
          <tr><td>(0028,0004)</td><td>CS</td><td>Photometric Interpretation</td><td>MONOCHROME2</td></tr>
          <tr><td>(0002,0010)</td><td>UI</td><td>Transfer Syntax</td><td>1.2.840.10008.1.2.1 (Explicit VR LE)</td></tr>
        </tbody>
      </table>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
    </div>
  `);
}

// Modal Helper
function showModal(title, htmlBody) {
  closeModal();
  const modal = document.createElement('div');
  modal.id = 'activeAppModal';
  modal.className = 'modal-backdrop';
  modal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">${title}</h3>
        <button class="btn btn-secondary btn-sm" onclick="closeModal()">✕</button>
      </div>
      <div class="modal-body">${htmlBody}</div>
    </div>
  `;
  document.body.appendChild(modal);
}

function closeModal() {
  const modal = document.getElementById('activeAppModal');
  if (modal) modal.remove();
}

// Tenant and Role Switchers
function onTenantChange(tenantCode) {
  AppState.currentTenant = tenantCode;
  Toast.show(`Switched Tenant Context to [${tenantCode}]`, 'warning');
  switchView(AppState.activeView);
}

function onRoleChange(role) {
  AppState.currentRole = role;
  Toast.show(`Role changed to ${role}`);
  switchView(AppState.activeView);
}

// Initial Boot
window.addEventListener('DOMContentLoaded', () => {
  switchView('lab-dashboard');
});
