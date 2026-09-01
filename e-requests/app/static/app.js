// HRep e-Request Portal Frontend Application

let currentServices = [];
let selectedService = null;
let currentTriageData = null;

// Initialize on Load
document.addEventListener("DOMContentLoaded", async () => {
    await loadUserProfile();
    await loadServices();
    await loadRequests();
});

// 1. User Profile
async function loadUserProfile() {
    try {
        const res = await fetch("/api/auth/me");
        const user = await res.json();
        document.getElementById("user-name").textContent = user.full_name;
        document.getElementById("user-role").textContent = `${user.role} • ${user.position || ''}`;
        
        const envBadge = document.getElementById("env-badge");
        if (user.app_env === "production") {
            envBadge.className = "px-2.5 py-1 text-xs font-semibold rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/40";
            envBadge.innerHTML = `<i class="fa-solid fa-cloud text-[8px] mr-1 text-blue-400"></i> Google Cloud Prod`;
        }
    } catch (e) {
        console.error("Auth error:", e);
    }
}

// 2. Tab Navigation
function switchTab(tabId) {
    ["catalog", "requests", "approvals", "agent"].forEach(t => {
        const view = document.getElementById(`view-${t}`);
        const tabBtn = document.getElementById(`tab-${t}`);
        if (t === tabId) {
            view.classList.remove("hidden");
            tabBtn.className = "py-3 px-1 border-b-2 border-amber-500 text-slate-900 font-semibold text-sm flex items-center space-x-2";
        } else {
            view.classList.add("hidden");
            tabBtn.className = "py-3 px-1 border-b-2 border-transparent text-slate-500 hover:text-slate-700 font-medium text-sm flex items-center space-x-2";
        }
    });

    if (tabId === "requests") loadRequests();
    if (tabId === "approvals") loadApprovals();
}

// 3. Service Catalog Loading & Filtering
async function loadServices(deptCode = "") {
    try {
        let url = "/api/services/";
        if (deptCode) url += `?department_code=${deptCode}`;
        const res = await fetch(url);
        currentServices = await res.json();
        renderServicesGrid(currentServices);
    } catch (e) {
        console.error("Failed to load services:", e);
    }
}

function filterServices() {
    const dept = document.getElementById("dept-filter").value;
    loadServices(dept);
}

function getDeptIcon(code) {
    switch (code) {
        case "ADMIN": return { icon: "fa-van-shuttle", color: "bg-blue-100 text-blue-800" };
        case "EPFD": return { icon: "fa-screwdriver-wrench", color: "bg-amber-100 text-amber-800" };
        case "ICTS": return { icon: "fa-laptop-code", color: "bg-indigo-100 text-indigo-800" };
        case "OSAA": return { icon: "fa-id-badge", color: "bg-emerald-100 text-emerald-800" };
        case "LAD": return { icon: "fa-scale-balanced", color: "bg-purple-100 text-purple-800" };
        default: return { icon: "fa-file-lines", color: "bg-slate-100 text-slate-800" };
    }
}

function renderServicesGrid(services) {
    const grid = document.getElementById("services-grid");
    grid.innerHTML = "";

    services.forEach(s => {
        const badge = getDeptIcon(s.service_code.split("_")[0]);
        const card = document.createElement("div");
        card.className = "bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between";
        card.innerHTML = `
            <div>
                <div class="flex items-center justify-between mb-3">
                    <span class="p-2.5 rounded-lg ${badge.color}"><i class="fa-solid ${badge.icon} text-lg"></i></span>
                    <span class="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-600">SLA: ${s.sla_hours} hrs</span>
                </div>
                <h3 class="text-base font-bold text-slate-900 mb-1">${s.service_name}</h3>
                <p class="text-xs text-slate-500 line-clamp-3 mb-4">${s.description}</p>
            </div>
            <button onclick="openFormModal('${s.id}')" class="w-full py-2 bg-slate-900 hover:bg-amber-500 hover:text-slate-900 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center space-x-1.5">
                <span>Start Request</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
            </button>
        `;
        grid.appendChild(card);
    });
}

// 4. Dynamic Form Generation from JSON Schema
function openFormModal(serviceId, prefillData = null) {
    selectedService = currentServices.find(s => s.id === serviceId);
    if (!selectedService) return;

    document.getElementById("modal-dept-code").textContent = selectedService.service_code.split("_")[0];
    document.getElementById("modal-service-title").textContent = selectedService.service_name;

    const form = document.getElementById("dynamic-form");
    form.innerHTML = "";

    const schema = selectedService.form_schema;
    if (schema && schema.fields) {
        schema.fields.forEach(field => {
            const fieldWrapper = document.createElement("div");
            const val = prefillData && prefillData[field.name] !== undefined ? prefillData[field.name] : '';

            let inputHtml = "";
            if (field.type === "select") {
                const optionsHtml = field.options.map(opt => `<option value="${opt}" ${opt === val ? 'selected' : ''}>${opt}</option>`).join("");
                inputHtml = `
                    <select name="${field.name}" ${field.required ? 'required' : ''} class="w-full text-sm border border-slate-300 rounded-lg p-2.5 bg-white focus:ring-2 focus:ring-amber-500">
                        <option value="">-- Select an option --</option>
                        ${optionsHtml}
                    </select>
                `;
            } else if (field.type === "textarea") {
                inputHtml = `
                    <textarea name="${field.name}" ${field.required ? 'required' : ''} rows="3" placeholder="${field.placeholder || ''}" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-amber-500">${val}</textarea>
                `;
            } else {
                inputHtml = `
                    <input type="${field.type}" name="${field.name}" value="${val}" ${field.required ? 'required' : ''} placeholder="${field.placeholder || ''}" min="${field.min || ''}" max="${field.max || ''}" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-amber-500">
                `;
            }

            fieldWrapper.innerHTML = `
                <label class="block text-xs font-bold text-slate-700 mb-1">
                    ${field.label} ${field.required ? '<span class="text-rose-500">*</span>' : ''}
                </label>
                ${inputHtml}
            `;
            form.appendChild(fieldWrapper);
        });
    }

    document.getElementById("modal-form").classList.remove("hidden");
}

function closeFormModal() {
    document.getElementById("modal-form").classList.add("hidden");
    selectedService = null;
}

// 5. Submit Dynamic Form
async function submitForm(e) {
    e.preventDefault();
    if (!selectedService) return;

    const formDataObj = {};
    const formData = new FormData(e.target);
    for (let [key, value] of formData.entries()) {
        formDataObj[key] = value;
    }

    try {
        const res = await fetch("/api/requests/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                service_id: selectedService.id,
                form_data: formDataObj,
                priority: "Normal"
            })
        });

        if (res.ok) {
            const data = await res.json();
            alert(`✅ Request submitted successfully!\nTracking Number: ${data.tracking_number}`);
            closeFormModal();
            switchTab("requests");
        } else {
            alert("❌ Failed to submit request.");
        }
    } catch (e) {
        console.error("Submission error:", e);
    }
}

// 6. Track Requests Table
async function loadRequests() {
    try {
        const res = await fetch("/api/requests/");
        const requests = await res.json();
        document.getElementById("req-count-badge").textContent = requests.length;

        const tbody = document.getElementById("requests-tbody");
        tbody.innerHTML = "";

        requests.forEach(r => {
            let statusBadge = "bg-slate-100 text-slate-700";
            if (r.status === "Approved") statusBadge = "bg-emerald-100 text-emerald-800";
            if (r.status === "Pending Approval") statusBadge = "bg-amber-100 text-amber-800";
            if (r.status === "In Progress") statusBadge = "bg-blue-100 text-blue-800";
            if (r.status === "Completed") statusBadge = "bg-purple-100 text-purple-800";

            const row = document.createElement("tr");
            row.className = "hover:bg-slate-50";
            row.innerHTML = `
                <td class="px-4 py-3 font-mono font-bold text-slate-900 text-xs">${r.tracking_number}</td>
                <td class="px-4 py-3">
                    <div class="font-semibold text-slate-800">${r.service_name}</div>
                    <div class="text-xs text-slate-400 font-mono">${r.department_code}</div>
                </td>
                <td class="px-4 py-3 text-xs">${r.requester_name}</td>
                <td class="px-4 py-3 text-xs font-semibold ${r.priority === 'Urgent' ? 'text-rose-600' : 'text-slate-600'}">${r.priority}</td>
                <td class="px-4 py-3"><span class="px-2 py-0.5 rounded text-xs font-semibold ${statusBadge}">${r.status}</span></td>
                <td class="px-4 py-3 text-xs text-slate-500">${new Date(r.submitted_at).toLocaleDateString()}</td>
                <td class="px-4 py-3 text-right">
                    <button onclick="viewRequestDetail('${r.id}')" class="px-2.5 py-1 text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded">View Detail</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (e) {
        console.error("Failed to load requests:", e);
    }
}

// 7. Request Detail & Audit Modal
async function viewRequestDetail(id) {
    try {
        const res = await fetch(`/api/requests/${id}`);
        const data = await res.json();

        document.getElementById("detail-tracking-no").textContent = data.tracking_number;
        document.getElementById("detail-title").textContent = data.service_name;

        const content = document.getElementById("detail-content");
        
        let formDataHtml = Object.entries(data.form_data).map(([k, v]) => `
            <div class="bg-slate-50 p-2.5 rounded border border-slate-100">
                <span class="text-[11px] font-bold text-slate-400 uppercase">${k.replace(/_/g, ' ')}:</span>
                <p class="text-xs font-medium text-slate-800 mt-0.5">${v}</p>
            </div>
        `).join("");

        let approvalsHtml = data.approvals.map(a => `
            <div class="p-3 rounded-lg border ${a.status === 'Approved' ? 'bg-emerald-50 border-emerald-200' : 'bg-amber-50 border-amber-200'}">
                <div class="flex justify-between items-center text-xs">
                    <span class="font-bold">${a.approver_name}</span>
                    <span class="font-bold uppercase ${a.status === 'Approved' ? 'text-emerald-700' : 'text-amber-700'}">${a.status}</span>
                </div>
                ${a.digital_stamp ? `<p class="text-[10px] font-mono text-slate-500 mt-1 break-all">🔒 Stamp: ${a.digital_stamp}</p>` : ''}
            </div>
        `).join("");

        let auditHtml = data.audit_logs.map(log => `
            <li class="text-xs text-slate-600 flex justify-between py-1 border-b border-slate-100">
                <span><strong>${log.action}</strong> by ${log.actor}: ${log.details}</span>
                <span class="text-slate-400 text-[10px]">${new Date(log.timestamp).toLocaleTimeString()}</span>
            </li>
        `).join("");

        content.innerHTML = `
            <div>
                <h4 class="font-bold text-slate-900 mb-2">Submitted Field Data</h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">${formDataHtml}</div>
            </div>
            <div>
                <h4 class="font-bold text-slate-900 mb-2">Approval Chain</h4>
                <div class="space-y-2">${approvalsHtml || '<p class="text-xs text-slate-400">No approval records yet.</p>'}</div>
            </div>
            <div>
                <h4 class="font-bold text-slate-900 mb-2">Immutable Audit Log</h4>
                <ul class="space-y-1">${auditHtml}</ul>
            </div>
        `;

        document.getElementById("modal-detail").classList.remove("hidden");
    } catch (e) {
        console.error("Detail error:", e);
    }
}

function closeDetailModal() {
    document.getElementById("modal-detail").classList.add("hidden");
}

// 8. Executive Approvals Workbench
async function loadApprovals() {
    try {
        const res = await fetch("/api/requests/");
        const requests = await res.json();
        const pending = requests.filter(r => r.status === "Pending Approval");

        const container = document.getElementById("approvals-container");
        container.innerHTML = "";

        if (pending.length === 0) {
            container.innerHTML = `
                <div class="text-center py-12 bg-white rounded-xl border border-slate-200">
                    <i class="fa-solid fa-clipboard-check text-4xl text-emerald-500 mb-2"></i>
                    <p class="text-sm font-semibold text-slate-700">All pending approvals are cleared!</p>
                </div>
            `;
            return;
        }

        pending.forEach(r => {
            const card = document.createElement("div");
            card.className = "bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4";
            card.innerHTML = `
                <div>
                    <div class="flex items-center space-x-2">
                        <span class="text-xs font-mono font-bold bg-amber-100 text-amber-900 px-2 py-0.5 rounded">${r.tracking_number}</span>
                        <span class="text-sm font-bold text-slate-900">${r.service_name}</span>
                    </div>
                    <p class="text-xs text-slate-500 mt-1">Requested by: <strong>${r.requester_name}</strong> • Submitted: ${new Date(r.submitted_at).toLocaleString()}</p>
                </div>
                <div class="flex items-center space-x-2 w-full md:w-auto">
                    <button onclick="approveTicket('${r.id}', 'Rejected')" class="px-4 py-2 text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 rounded-lg border border-rose-200">Reject</button>
                    <button onclick="approveTicket('${r.id}', 'Approved')" class="px-5 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow flex items-center space-x-1.5">
                        <i class="fa-solid fa-signature"></i>
                        <span>Digitally Sign & Approve</span>
                    </button>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (e) {
        console.error("Failed to load approvals:", e);
    }
}

async function approveTicket(id, action) {
    try {
        const res = await fetch(`/api/requests/${id}/action`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: action, remarks: "Authenticated Executive Sign-Off" })
        });
        if (res.ok) {
            alert(`✅ Ticket ${action.toUpperCase()} successfully!`);
            loadApprovals();
        }
    } catch (e) {
        console.error("Action error:", e);
    }
}

// 9. ADK AI Triage Agent
function setPrompt(txt) {
    document.getElementById("agent-input").value = txt;
}

async function runTriage() {
    const input = document.getElementById("agent-input").value.trim();
    if (!input) return;

    const btn = document.getElementById("btn-triage");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...`;

    try {
        const res = await fetch("/api/agent/triage", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_prompt: input })
        });

        const data = await res.json();
        currentTriageData = data;

        document.getElementById("triage-empty").classList.add("hidden");
        document.getElementById("triage-result").classList.remove("hidden");

        document.getElementById("triage-service-name").textContent = data.suggested_service_name;
        document.getElementById("triage-confidence").textContent = `${Math.round(data.confidence_score * 100)}%`;
        document.getElementById("triage-json").textContent = JSON.stringify(data.extracted_fields, null, 2);

        const nextQContainer = document.getElementById("triage-next-q-container");
        if (data.next_question) {
            document.getElementById("triage-next-q").textContent = data.next_question;
            nextQContainer.classList.remove("hidden");
        } else {
            nextQContainer.classList.add("hidden");
        }
    } catch (e) {
        console.error("Triage error:", e);
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<span>Analyze Request</span> <i class="fa-solid fa-arrow-right text-xs"></i>`;
    }
}

function launchPrefilledForm() {
    if (!currentTriageData) return;
    const targetService = currentServices.find(s => s.service_code === currentTriageData.suggested_service_code);
    if (targetService) {
        openFormModal(targetService.id, currentTriageData.extracted_fields);
    }
}
