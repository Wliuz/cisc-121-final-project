import gradio as gr


class InsertionSortVisualizer:
    """
    Insertion sort driven entirely by the user (YES/NO per comparison).
    Key design decision that eliminates the bar-height flicker bug:
    - self.arr is NEVER partially mutated during a pass.
    - A separate self.display list (always full-length) is what the bars read.
    - self.max_val is locked at start time and never recomputed.
    """

    def __init__(self):
        self._reset_state()

    def _reset_state(self):
        self.arr = []        # working array — only written when a pass finishes
        self.display = []    # what the bars show (always same length as arr)
        self.max_val = 1     # locked at sort-start; bar heights never rescale
        self.n = 0

        self.i = 1           # outer pass counter
        self.hole = 1        # current position of the "hole" / temp element
        self.temp = None     # value being inserted this pass

        self.sort_complete = False
        self.sort_correct = False   # NEW: was the final array actually sorted?
        self.log = []
        self.message = ""

        self.cmp_left = -1   # indices highlighted orange
        self.cmp_right = -1

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self):
        if not self.display:
            return "<div style='text-align:center;padding:60px;font-family:monospace;color:#555;'>Enter numbers and click Start!</div>"

        bars = (
            '<div style="display:flex;align-items:flex-end;justify-content:center;'
            'gap:12px;padding:24px 20px 0;background:#1e1e2e;border-radius:12px 12px 0 0;min-height:320px;">'
        )

        for idx, val in enumerate(self.display):
            # Priority: done states first, then per-element roles
            if self.sort_complete and self.sort_correct:
                color, label_color = "#2ecc71", "#2ecc71"
            elif self.sort_complete and not self.sort_correct:
                color, label_color = "#e74c3c", "#e74c3c"   # red = wrong final order
            elif idx == self.hole and not self.sort_complete:
                # The element being inserted is ALWAYS red, even during a comparison
                color, label_color = "#e74c3c", "#e74c3c"
            elif idx == self.cmp_left:
                # Only the left neighbour being compared against turns orange
                color, label_color = "#f5a623", "#f5a623"
            elif idx < self.i:
                color, label_color = "#3498db", "#3498db"
            else:
                color, label_color = "#636e72", "#b2bec3"

            height_px = max(int((val / self.max_val) * 240), 6)

            bars += (
                f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;">'
                f'<div style="font-family:\'Courier New\',monospace;font-size:13px;font-weight:700;color:{label_color};">{val}</div>'
                f'<div style="width:52px;height:{height_px}px;background:{color};border-radius:4px 4px 0 0;'
                f'box-shadow:0 0 12px {color}55;transition:height 0.25s ease,background 0.2s ease;"></div>'
                f'<div style="font-family:\'Courier New\',monospace;font-size:11px;color:#636e72;padding-bottom:8px;">[{idx}]</div>'
                f'</div>'
            )

        bars += "</div>"

        # Legend reflects the two possible "done" states
        if self.sort_complete and not self.sort_correct:
            done_entry = ("#e74c3c", "Incorrectly Sorted ⚠️")
        else:
            done_entry = ("#2ecc71", "Complete ✅")

        legend = (
            '<div style="display:flex;justify-content:center;flex-wrap:wrap;gap:18px;padding:14px 20px;'
            'background:#181825;border-radius:0 0 12px 12px;border-top:1px solid #313244;">'
        )
        for hex_color, label in [
            ("#3498db", "Sorted"),
            ("#e74c3c", "Currently Inserting"),
            ("#f5a623", "Neighbour Being Compared"),
            ("#636e72", "Unsorted"),
            done_entry,
        ]:
            legend += (
                f'<span style="font-family:\'Courier New\',monospace;font-size:13px;color:#cdd6f4;'
                f'display:flex;align-items:center;gap:6px;">'
                f'<span style="display:inline-block;width:14px;height:14px;background:{hex_color};border-radius:2px;"></span>'
                f'{label}</span>'
            )
        legend += "</div>"

        return bars + legend

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sync_display(self):
        """
        Rebuild display so every bar shows its correct value.
        During an active pass the hole position shows self.temp,
        not whatever placeholder may be sitting in self.arr[hole].
        """
        self.display = list(self.arr)
        if not self.sort_complete and self.temp is not None:
            self.display[self.hole] = self.temp

    def _ask_comparison(self):
        """
        Decide whether to ask the user about the element left of the hole,
        or whether temp has found its final resting place.
        """
        left = self.hole - 1
        if left >= 0 and self.temp < self.arr[left]:
            self.cmp_left = left
            self.cmp_right = self.hole
            self.message = f"Should we swap {self.temp} with {self.arr[left]}?"
        else:
            self._finish_pass()

    def _finish_pass(self):
        """Write temp into the hole, then start the next pass (or finish)."""
        self.arr[self.hole] = self.temp
        self.cmp_left = self.cmp_right = -1
        self.log.append(f"📌 Placed {self.temp} at index {self.hole}  →  {list(self.arr)}")
        self.i += 1
        if self.i >= self.n:
            self.sort_complete = True
            # NEW: check whether the user's answers actually produced a sorted array
            self.sort_correct = all(self.arr[k] <= self.arr[k + 1] for k in range(self.n - 1))
            if self.sort_correct:
                self.message = f"🎉 Sorting complete!  Final: {list(self.arr)}"
            else:
                self.message = (
                    f"⚠️ Sort finished but the array is NOT correctly sorted!\n"
                    f"Result: {list(self.arr)}\n"
                    f"You may have answered NO when you should have said YES."
                )
            self.log.append(self.message)
        else:
            self._begin_pass()

    def _begin_pass(self):
        """Set up the outer-loop pass for index self.i."""
        self.temp = self.arr[self.i]
        self.hole = self.i
        self._ask_comparison()

    # ------------------------------------------------------------------
    # Public interface called by Gradio
    # ------------------------------------------------------------------

    def start_sort(self, text):
        self._reset_state()
        try:
            nums = [int(x.strip()) for x in text.split(",") if x.strip()]
        except ValueError:
            return None, "❌ Use comma-separated integers, e.g.  5,2,8,1,9", ""

        if len(nums) < 2:
            return None, "❌ Please enter at least 2 numbers.", ""
        if len(nums) > 10:
            return None, "⚠️ Please use 10 numbers or fewer for a clear display.", ""

        self.arr = nums
        self.n = len(nums)
        self.max_val = max(nums)   # locked forever — heights never change scale
        self.log = [f"🟢 Start: {list(self.arr)}"]

        self._begin_pass()
        self._sync_display()
        return self._render(), self.message, "\n".join(self.log)

    def answer(self, yes: bool):
        if not self.arr:
            return self._render(), "⚠️ Please enter numbers and click Start Sorting first.", "\n".join(self.log)
        if self.sort_complete:
            return self._render(), "🎉 Already complete — press Reset to start over.", "\n".join(self.log)

        if yes:
            left = self.hole - 1
            # Shift the left neighbour into the hole (arr mutation is safe here
            # because _sync_display will overwrite arr[hole] with temp before render)
            self.arr[self.hole] = self.arr[left]
            self.log.append(f"✅ YES — shifted {self.arr[left]} right, hole moves to [{left}]")
            self.hole -= 1
            self._ask_comparison()
        else:
            self.log.append(f"❌ NO  — {self.temp} stays at index {self.hole}")
            self._finish_pass()

        self._sync_display()
        return self._render(), self.message, "\n".join(self.log)

    def reset(self):
        self._reset_state()
        return (
            "<div style='text-align:center;padding:60px;font-family:monospace;color:#888;'>"
            "Enter numbers and click Start!</div>",
            "Reset — enter a new array and click Start Sorting.",
            "",
        )


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

def build_ui():
    css = """
    .gradio-container { max-width: 1100px !important; margin: auto; }
    #bar_chart { background: transparent !important; border: none !important; }
    """

    sorter = InsertionSortVisualizer()

    with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
        gr.Markdown("""
# 🎮 Interactive Insertion Sort
Control every swap yourself — watch the bars respond in real time.
| Colour | Meaning |
|--------|---------|
| 🔵 Blue | Already sorted |
| 🔴 Red | Being inserted right now (or incorrectly sorted result) |
| 🟠 Orange | Left neighbour currently being compared against |
| ⚫ Grey | Not yet reached |
| 🟢 Green | Sorting complete and correct |
""")

        with gr.Row():
            with gr.Column(scale=3):
                array_input = gr.Textbox(
                    label="Numbers (comma-separated)",
                    placeholder="e.g.  5, 2, 8, 1, 9, 3, 7",
                    value="5,2,8,1,9,3,7",
                )
                with gr.Row():
                    start_btn = gr.Button("🚀 Start Sorting", variant="primary")
                    reset_btn = gr.Button("🔄 Reset", variant="secondary")
            with gr.Column(scale=2):
                status = gr.Textbox(label="Status", interactive=False, lines=3)

        bar_chart = gr.HTML(elem_id="bar_chart")

        with gr.Row():
            yes_btn = gr.Button("✅  YES — Swap", variant="primary", size="lg")
            no_btn  = gr.Button("❌  NO — Keep",  variant="stop",    size="lg")

        log_box = gr.Textbox(label="Step log", interactive=False, lines=10)

        gr.Examples(
            examples=[["5,2,8,1,9"], ["10,3,7,1,5,2"], ["9,8,7,6,5"], ["1,2,3,4,5"]],
            inputs=array_input,
        )

        start_btn.click(lambda t: sorter.start_sort(t), [array_input], [bar_chart, status, log_box])
        yes_btn.click(lambda: sorter.answer(True),  [], [bar_chart, status, log_box])
        no_btn.click( lambda: sorter.answer(False), [], [bar_chart, status, log_box])
        reset_btn.click(lambda: sorter.reset(),     [], [bar_chart, status, log_box])

    return demo


if __name__ == "__main__":
    build_ui().launch()
