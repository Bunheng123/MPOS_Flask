document.addEventListener('DOMContentLoaded', () => {
  const sidebar   = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('sidebarToggle');
  const backdrop  = document.getElementById('sidebarBackdrop');

  // ---- Mobile drawer helpers (lg breakpoint is 1024px) ----
  function openMobileSidebar() {
    if (sidebar) sidebar.classList.add('mobile-open');
    if (backdrop) backdrop.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileSidebar() {
    if (sidebar) sidebar.classList.remove('mobile-open');
    if (backdrop) backdrop.classList.remove('show');
    document.body.style.overflow = '';
  }

  // ---- Toggle button ----
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      if (window.innerWidth <= 1023) {
        sidebar.classList.contains('mobile-open') ? closeMobileSidebar() : openMobileSidebar();
      } else {
        // Collapse / expand on desktop
        sidebar.classList.toggle('collapsed');
      }
    });
  }

  // ---- Tap backdrop to close on mobile ----
  if (backdrop) {
    backdrop.addEventListener('click', closeMobileSidebar);
  }

  // ---- Resize: clean up mobile state when returning to desktop ----
  window.addEventListener('resize', () => {
    if (window.innerWidth > 1023) {
      closeMobileSidebar();
      document.body.style.overflow = '';
    }
  });

  // ---- Chart tab buttons (dashboard) ----
  document.querySelectorAll('.panel-tabs button').forEach(btn => {
    btn.addEventListener('click', () => {
      const container = btn.closest('.flex');
      if (container) {
        container.querySelectorAll('button').forEach(t => {
          t.classList.remove('bg-card', 'text-text', 'shadow-sm');
          t.classList.add('bg-transparent', 'text-text-muted');
        });
      }
      btn.classList.remove('bg-transparent', 'text-text-muted');
      btn.classList.add('bg-card', 'text-text', 'shadow-sm');
    });
  });

  // ---- Dropdown Menus (click outside to close) ----
  document.addEventListener('click', (e) => {
    // 1. User Profile Chip Dropdown
    const userChip = document.getElementById('navUserChip');
    const userDropdown = document.getElementById('navUserDropdown');
    if (userChip && userDropdown) {
      if (userChip.contains(e.target)) {
        userDropdown.classList.toggle('hidden');
      } else if (!userDropdown.contains(e.target)) {
        userDropdown.classList.add('hidden');
      }
    }

    // 2. Users Page Role Dropdown
    const roleBtn = document.getElementById('roleFilterBtn');
    const roleDropdown = document.getElementById('roleFilterDropdown');
    if (roleBtn && roleDropdown) {
      if (roleBtn.contains(e.target)) {
        roleDropdown.classList.toggle('hidden');
      } else if (!roleDropdown.contains(e.target)) {
        roleDropdown.classList.add('hidden');
      }
    }
  });

  // ---- Image Upload Instant Preview (Add / Edit User) ----
  const profileImageInput = document.getElementById('profileImageInput');
  const profilePreview = document.getElementById('profilePreview');
  const defaultAvatarIcon = document.getElementById('defaultAvatarIcon');
  const fileNameDisplay = document.getElementById('fileNameDisplay');
  const uploadButtonText = document.getElementById('uploadButtonText');

  if (profileImageInput && profilePreview) {
    let currentObjectUrl = null;

    profileImageInput.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];

      if (file) {
        if (currentObjectUrl) {
          URL.revokeObjectURL(currentObjectUrl);
        }

        currentObjectUrl = URL.createObjectURL(file);
        profilePreview.src = currentObjectUrl;
        profilePreview.classList.remove('hidden');

        if (defaultAvatarIcon) {
          defaultAvatarIcon.classList.add('hidden');
        }

        if (fileNameDisplay) {
          fileNameDisplay.textContent = file.name;
          fileNameDisplay.classList.remove('hidden');
        }

        if (uploadButtonText) {
          uploadButtonText.textContent = 'Change Photo';
        }
      } else {
        const originalSrc = profilePreview.getAttribute('data-original-src');
        if (originalSrc) {
          profilePreview.src = originalSrc;
          profilePreview.classList.remove('hidden');
        } else if (defaultAvatarIcon) {
          profilePreview.src = '';
          profilePreview.classList.add('hidden');
          defaultAvatarIcon.classList.remove('hidden');
        }

        if (fileNameDisplay) {
          fileNameDisplay.textContent = '';
          fileNameDisplay.classList.add('hidden');
        }

        if (uploadButtonText) {
          uploadButtonText.textContent = 'Choose File';
        }
      }
    });
  }
});