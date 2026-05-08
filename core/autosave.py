"""Auto-save Module with debounce and fallback - Versão Estável"""

from PySide6.QtCore import QTimer, QObject, Signal
import logging

logger = logging.getLogger(__name__)


class AutoSaveManager(QObject):
    """Manages auto-save with debounce and emergency fallback"""
    
    # Sinal correto para o auto-save
    auto_save = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self._on_debounce_timeout)
        
        self.periodic_timer = QTimer()
        self.periodic_timer.timeout.connect(self._on_periodic_timeout)
        
        self.debounce_delay = 1500  # 1.5 seconds after typing stops
        self.save_interval = 30000  # 30 seconds max between saves
        
        self.is_saving = False
        self.pending_save = False
        self.last_save_time = None
        
    def start(self, debounce_delay: int = 1500, save_interval: int = 30000):
        """Start auto-save timers"""
        self.debounce_delay = debounce_delay
        self.save_interval = save_interval
        self.periodic_timer.start(save_interval)
        logger.info(f"Auto-save started: debounce={debounce_delay}ms, interval={save_interval}ms")
        
    def stop(self):
        """Stop auto-save timers"""
        self.debounce_timer.stop()
        self.periodic_timer.stop()
        logger.info("Auto-save stopped")
        
    def content_changed(self):
        """Called when content changes - triggers debounce"""
        if not self.is_saving:
            self.debounce_timer.start(self.debounce_delay)
            self.pending_save = True
            
    def _on_debounce_timeout(self):
        """Debounce timer expired - user stopped typing"""
        if self.pending_save and not self.is_saving:
            logger.debug("Debounce timeout - triggering auto-save")
            self._trigger_save()
            
    def _on_periodic_timeout(self):
        """Periodic save - even if user still typing"""
        if self.pending_save and not self.is_saving:
            logger.debug("Periodic timeout - triggering auto-save")
            self._trigger_save()
            
    def _trigger_save(self):
        """Trigger the actual save operation"""
        self.pending_save = False
        self.auto_save.emit()  # Emitindo o sinal correto
        
    def save_completed(self, success: bool):
        """Called after save completes"""
        self.is_saving = False
        if success:
            self.pending_save = False
            self.last_save_time = QTimer().remainingTime() if hasattr(QTimer(), 'remainingTime') else None
            logger.debug("Auto-save completed successfully")
        else:
            # Keep pending_save True to retry
            self.pending_save = True
            logger.warning("Auto-save failed, will retry")
            
    def force_save(self):
        """Force immediate save"""
        self.debounce_timer.stop()
        if not self.is_saving:
            logger.info("Force save triggered")
            self._trigger_save()
    
    def reset(self):
        """Reset auto-save state"""
        self.debounce_timer.stop()
        self.pending_save = False
        self.is_saving = False