import asyncio
import uuid
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.runners import types
from .agent import create_inventory_agent

# Load environment variables from .env file
load_dotenv()

async def run_simulation():
    print("--- Starting Inventory Simulation ---")
    
    agent = create_inventory_agent()
    session_service = InMemorySessionService()
    app_name = "inventory_app"
    
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service
    )
    
    prompt_text = "Please check the stock for 'Laptop'. If it is low, order enough to reach 20 units and update our records."
    print(f"\nUser Request: {prompt_text}\n")
    
    part = types.Part(text=prompt_text)
    content = types.Content(role="user", parts=[part])
    
    session_id = str(uuid.uuid4())
    user_id = "user-1"
    
    try:
        # Create session explicitly
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        print("--- Agent Execution ---\n")
        
        turn_count = 0
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            # Each event has a content attribute with parts
            if hasattr(event, 'content') and event.content:
                parts = event.content.parts
                
                # Track if this is an agent turn
                has_text = any(hasattr(p, 'text') and p.text for p in parts)
                has_function_call = any(hasattr(p, 'function_call') for p in parts)
                has_function_response = any(hasattr(p, 'function_response') for p in parts)
                
                if has_text or has_function_call:
                    turn_count += 1
                    print(f"\n{'='*60}")
                    print(f"Turn {turn_count}")
                    print(f"{'='*60}")
                
                for part in parts:
                    # Print agent's reasoning/text
                    if hasattr(part, 'text') and part.text:
                        print(f"\n💭 Agent Thinking:\n{part.text}")
                    
                    # Print tool calls
                    if hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        if hasattr(fc, 'args') and fc.args:
                            args_str = ", ".join(f"{k}={repr(v)}" for k, v in fc.args.items())
                        else:
                            args_str = ""
                        name = fc.name if hasattr(fc, 'name') else str(fc)
                        print(f"\n🔧 Tool Call: {name}({args_str})")
                    
                    # Print tool responses
                    if hasattr(part, 'function_response') and part.function_response:
                        fr = part.function_response 
                        # Get the actual response data
                        if hasattr(fr, 'response'):
                            result = fr.response
                        elif hasattr(fr, '__dict__'):
                            result = fr.__dict__
                        else:
                            result = str(fr)
                        print(f"✓ Tool Result:\n{result}")

        print(f"\n\n{'='*60}")
        print("--- Simulation Complete ---")
        print(f"Total Turns: {turn_count}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"Error running agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_simulation())
