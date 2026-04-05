import gradio as gr

class InteractiveInsertionSort:
    def __init__(self):
        self.arr = []
        self.i = 1
        self.j = 0
        self.temp = None
        self.step_log = []
        self.sort_complete = False
        self.waiting_for_input = False
    
    def start_sort(self, arr_input):
        """Initialize the sorting process"""
        try:
            self.arr = [int(x.strip()) for x in arr_input.split(',')]
            self.i = 1
            self.temp = self.arr[1] if len(self.arr) > 1 else None
            self.j = self.i - 1
            self.step_log = [f"🟢 Started with array: {self.arr}"]
            self.sort_complete = False
            self.waiting_for_input = True
            
            return self.get_current_state(), "Ready to start sorting! Click 'Next Step'"
        except:
            return None, "❌ Invalid input. Use comma-separated numbers like: 5,2,8,1,9"
    
    def get_current_state(self):
        """Get current visualization state"""
        if self.sort_complete:
            return {
                "array": self.arr,
                "sorted_portion": self.arr,
                "current_element": None,
                "comparing_with": None,
                "is_complete": True
            }
        
        # Visual indicators
        sorted_until = self.i
        comparing_idx = self.j if self.j >= 0 else None
        
        return {
            "array": self.arr,
            "sorted_portion": self.arr[:sorted_until],
            "current_element": self.temp,
            "comparing_with": self.arr[self.j] if self.j >= 0 else None,
            "comparing_index": self.j,
            "is_complete": False
        }
    
    def make_swap(self, should_swap):
        """User decides YES or NO to swap"""
        if self.sort_complete:
            return self.get_current_state(), "Sorting already complete!"
        
        if not self.waiting_for_input:
            return self.get_current_state(), "Please start a new sort first!"
        
        if should_swap == "yes":
            # Perform the swap
            self.arr[self.j + 1] = self.arr[self.j]
            self.step_log.append(f"✓ Swapped: Moved {self.arr[self.j]} to position {self.j+1}")
            self.j -= 1
            
            # Check if we need to continue comparing
            if self.j >= 0 and self.temp < self.arr[self.j]:
                self.waiting_for_input = True
                message = f"Should we swap {self.temp} with {self.arr[self.j]}?"
            else:
                # Place temp in correct position
                self.arr[self.j + 1] = self.temp
                self.step_log.append(f"📌 Placed {self.temp} at position {self.j+1}")
                self.step_log.append(f"Array after pass {self.i}: {self.arr}")
                
                # Move to next element
                self.i += 1
                if self.i < len(self.arr):
                    self.temp = self.arr[self.i]
                    self.j = self.i - 1
                    self.waiting_for_input = True
                    message = f"Now inserting element {self.temp} from position {self.i}"
                else:
                    self.sort_complete = True
                    self.waiting_for_input = False
                    message = f"🎉 Sorting complete! Final array: {self.arr}"
        else:  # User said NO
            # Place temp at current position and move to next element
            self.arr[self.j + 1] = self.temp
            self.step_log.append(f"✗ No swap. Placed {self.temp} at position {self.j+1}")
            self.step_log.append(f"Array after pass {self.i}: {self.arr}")
            
            # Move to next element
            self.i += 1
            if self.i < len(self.arr):
                self.temp = self.arr[self.i]
                self.j = self.i - 1
                self.waiting_for_input = True
                message = f"Now inserting element {self.temp} from position {self.i}"
            else:
                self.sort_complete = True
                self.waiting_for_input = False
                message = f"🎉 Sorting complete! Final array: {self.arr}"
        
        return self.get_current_state(), message
    
    def reset(self):
        """Reset the sort"""
        self.__init__()
        return None, "Reset complete! Enter a new array."

# Create Gradio Interface
def create_ui():
    sorter = InteractiveInsertionSort()
    
    with gr.Blocks(theme=gr.themes.Soft(), css="""
        .array-container { font-size: 24px; font-family: monospace; padding: 20px; }
        .sorted { color: green; font-weight: bold; }
        .current { color: red; font-weight: bold; background: yellow; }
        .comparing { color: orange; font-weight: bold; }
    """) as demo:
        
        gr.Markdown("""
        # 🎮 Interactive Insertion Sort Game
        
        ### You control each swap! Click YES or NO to guide the sorting process.
        
        **How it works:**
        1. Enter a comma-separated list of numbers
        2. Click "Start Sorting"
        3. The algorithm will ask: Should we swap?
        4. You decide YES or NO to control the sort!
        """)
        
        with gr.Row():
            with gr.Column():
                array_input = gr.Textbox(
                    label="📊 Enter Numbers",
                    placeholder="Example: 5,2,8,1,9",
                    value="5,2,8,1,9"
                )
                start_btn = gr.Button("🚀 Start Sorting", variant="primary")
                reset_btn = gr.Button("🔄 Reset", variant="secondary")
            
            with gr.Column():
                status = gr.Textbox(label="Status", interactive=False)
        
        # Visualization
        with gr.Row():
            array_display = gr.JSON(label="Current Array State")
        
        with gr.Row():
            yes_btn = gr.Button("✅ YES - Swap these elements", variant="primary", size="lg")
            no_btn = gr.Button("❌ NO - Don't swap", variant="stop", size="lg")
        
        with gr.Row():
            log_display = gr.Textbox(label="Step Log", lines=10, interactive=False)
        
        # Store state
        state = gr.State(sorter)
        
        # Event handlers
        start_btn.click(
            sorter.start_sort,
            inputs=[array_input],
            outputs=[array_display, status]
        ).then(
            lambda s: (s.get_current_state(), s.step_log),
            inputs=[state],
            outputs=[array_display, log_display]
        )
        
        yes_btn.click(
            lambda s: s.make_swap("yes"),
            inputs=[state],
            outputs=[array_display, status]
        ).then(
            lambda s: (s.get_current_state(), s.step_log),
            inputs=[state],
            outputs=[array_display, log_display]
        )
        
        no_btn.click(
            lambda s: s.make_swap("no"),
            inputs=[state],
            outputs=[array_display, status]
        ).then(
            lambda s: (s.get_current_state(), s.step_log),
            inputs=[state],
            outputs=[array_display, log_display]
        )
        
        reset_btn.click(
            lambda s: s.reset(),
            inputs=[state],
            outputs=[array_display, status]
        )
    
    return demo

# Launch the app
if __name__ == "__main__":
    demo = create_ui()
    demo.launch()
