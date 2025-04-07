import argparse
from app.authentication.enroll import Enrollment
from app.authentication.verify import Verifier

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Face Authentication CLI")
    parser.add_argument("--enroll", help="Enroll a user", action="store_true")
    parser.add_argument("--name", help="User name")
    parser.add_argument("--image", help="Image path")
    args = parser.parse_args()

    if args.enroll:
        # Enroll a user from the CLI
        enroller = Enrollment()
        enroller.enroll_user(args.name, args.image)
    else:
        # Verify a face from the CLI
        verifier = Verifier()
        embedding = EmbeddingGenerator().generate_embedding(args.image)
        print(f"Authenticated as: {verifier.verify_user(embedding)}")