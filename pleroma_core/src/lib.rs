use pyo3::prelude::*;

mod gearbox;
use gearbox::HarmonicGearbox;

/// The Iron Kernel Entry Point.
/// This function is called when Python runs `import pleroma_core`.
#[pymodule]
fn pleroma_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<HarmonicGearbox>()?;
    Ok(())
}