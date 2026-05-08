from core.notes import NoteManager

class VaultManager:
    def __init__(self, note_manager: NoteManager):
        self.note_manager = note_manager

    def save_draft(self, content: str) -> str:
        title = f"draft_{len(self.note_manager.list_notes('vault')) + 1}"
        return self.note_manager.create_note("vault", title, content)

    def list_drafts(self):
        return self.note_manager.list_notes("vault")

    def restore_draft(self, draft_id: str, target_folder: str, new_title: str = None, folder_password: str = None):
        draft = self.note_manager.get_note("vault", draft_id)
        if draft:
            title = new_title or draft["title"].replace("draft_", "")
            return self.note_manager.create_note(target_folder, title, draft["content"], folder_password)
        return None