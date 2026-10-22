"use strict";

// Client-side helper only. Server-side validation is authoritative (Principle IV).

const teacherSelect = document.getElementById("teacher");
const projectSelect = document.getElementById("project");
const projectStatus = document.getElementById("project-status");
const messageBox = document.getElementById("message");
const assignmentsBody = document.getElementById("assignments-body");
const form = document.getElementById("assignment-form");

let projectsById = {};
let teachersById = {};

function showMessage(text, ok) {
  messageBox.textContent = text;
  messageBox.className = "message " + (ok ? "ok" : "error");
}

async function loadTeachers() {
  const res = await fetch("/api/teachers");
  const data = await res.json();
  teachersById = {};
  teacherSelect.innerHTML = "";
  data.forEach((t) => {
    teachersById[t.id] = t;
    const opt = document.createElement("option");
    opt.value = t.id;
    opt.textContent = t.name;
    teacherSelect.appendChild(opt);
  });
}

async function loadProjects() {
  const res = await fetch("/api/projects");
  const data = await res.json();
  projectsById = {};
  projectSelect.innerHTML = "";
  data.forEach((p) => {
    projectsById[p.id] = p;
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = p.code + " - " + p.name;
    projectSelect.appendChild(opt);
  });
  updateProjectStatus();
}

function updateProjectStatus() {
  const p = projectsById[projectSelect.value];
  projectStatus.textContent = p ? p.status : "-";
}

async function loadAssignments() {
  const res = await fetch("/api/assignments");
  const data = await res.json();
  assignmentsBody.innerHTML = "";
  if (data.length === 0) {
    assignmentsBody.innerHTML =
      '<tr><td colspan="5" class="empty">Sin registros.</td></tr>';
    return;
  }
  data.forEach((a) => {
    const tr = document.createElement("tr");
    const teacher = teachersById[a.teacher_id];
    const project = projectsById[a.project_id];
    tr.innerHTML =
      "<td>" + a.id + "</td>" +
      "<td>" + (teacher ? teacher.name : a.teacher_id) + "</td>" +
      "<td>" + (project ? project.code : a.project_id) + "</td>" +
      "<td>" + a.hours + "</td>" +
      "<td>" + new Date(a.created_at).toLocaleString() + "</td>";
    assignmentsBody.appendChild(tr);
  });
}

projectSelect.addEventListener("change", updateProjectStatus);

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    teacher_id: parseInt(teacherSelect.value, 10),
    project_id: parseInt(projectSelect.value, 10),
    hours: parseInt(document.getElementById("hours").value, 10),
  };

  const res = await fetch("/api/assignments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (res.status === 201) {
    showMessage("Asignacion registrada correctamente.", true);
    await loadAssignments();
  } else {
    const err = await res.json();
    let detail = err.detail;
    if (Array.isArray(detail)) {
      detail = detail.map((d) => d.msg).join("; ");
    }
    showMessage("Rechazado (" + res.status + "): " + detail, false);
  }
});

async function init() {
  await loadTeachers();
  await loadProjects();
  await loadAssignments();
}

init();
