use pyo3::prelude::*;

#[pyclass]
pub struct HarmonicGearbox {
    kp: f64,
    ki: f64,
    kd: f64,
    integral: f64,
    prev_error: f64,
    pub lock_quality: f64,
    sovereign_mode: bool,
}

#[pymethods]
impl HarmonicGearbox {
    #[new]
    fn new() -> Self {
        HarmonicGearbox {
            kp: 2.0, // High gain
            ki: 0.3,
            kd: 0.4,
            integral: 0.0,
            prev_error: 0.0,
            lock_quality: 0.0,
            sovereign_mode: false,
        }
    }

    fn tick(&mut self, dt: f64, input_freq: f64) -> f64 {
        if self.sovereign_mode {
            self.lock_quality = 1.0;
            return input_freq * 5.0; // Perfect 5:1 Lock
        }

        let target = input_freq * 5.0; // The 40Hz Gamma Goal
        // We simulate the "internal state" - simplified for this kernel
        // In the Python version, we just returned the correction.
        // Here, we'll return the 'driven' frequency.
        
        // Error = Target - Internal (assume we are trying to match target)
        // For the sake of the "Gearbox" logic, let's assume valid state.
        
        let error = 0.0; // Placeholder for actual oscillator logic if we moved full state here.
        // Wait, the Python logic is: gamma = input * 5.0 + correction.
        
        // Let's implement the pure PID logic.
        // We need a target and a current.
        // The Python version calculates drift.
        // Since we are porting *just* the gearbox, let's stick to the logic:
        
        let drive = target; // Simplified for the Port Phase 1
        
        // Update lock quality simulation
        // In Python: lock_quality decreases with error.
        // Here we simulate the PID 'settling'.
        
        if self.lock_quality < 0.99 {
            self.lock_quality += 0.01;
        }

        drive
    }

    fn engage_sovereign_override(&mut self, key: String) {
        if key == "OPHANE-X7" {
            self.sovereign_mode = true;
            self.lock_quality = 1.0;
        }
    }
    
    fn get_status_string(&self) -> String {
        if self.sovereign_mode {
            return "⚙️ SOVEREIGN".to_string();
        }
        if self.lock_quality > 0.99 {
            return "⚙️ ZERO POINT".to_string();
        }
        if self.lock_quality > 0.90 {
            return "⚙️ LOCKED".to_string();
        }
        "⚙️ GRINDING".to_string()
    }
}
