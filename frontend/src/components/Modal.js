import React from 'react';
import ReactDOM from 'react-dom';

const modalRoot = document.getElementById('modal-root') || (() => {
  const el = document.createElement('div');
  el.id = 'modal-root';
  document.body.appendChild(el);
  return el;
})();

export default function Modal({ children, onClose }) {
  return ReactDOM.createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    modalRoot
  );
}
