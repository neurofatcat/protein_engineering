import os
import subprocess

def run_rf_diffusion(input_pdb, output_dir, num_designs=5, additional_args=None):
    """
    Execute RFdiffusion protocol for de novo protein design.

    Args:
        input_pdb (str): Path to the input PDB file.
        output_dir (str): Directory to save the output files.
        num_designs (int): Number of protein designs to generate.
        additional_args (list): Additional arguments for RFdiffusion.

    Returns:
        dict: Result containing success status, log, and output files.
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Define the output path
        output_pdb = os.path.join(output_dir, f"designed_{os.path.basename(input_pdb)}")

        # Construct the RFdiffusion command
        command = [
            "python", "run_RFdiffusion.py",
            "--input", input_pdb,
            "--output", output_pdb,
            "--num_designs", str(num_designs)
        ]
        if additional_args:
            command.extend(additional_args)

        # Run the command
        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode == 0:
            return {
                "success": True,
                "log": process.stdout,
                "output_pdb": output_pdb
            }
        else:
            return {
                "success": False,
                "log": process.stderr
            }
    except Exception as e:
        return {
            "success": False,
            "log": str(e)
        }
