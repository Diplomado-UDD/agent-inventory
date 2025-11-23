import asyncio
import uuid
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.runners import types
from inventory_system.agent import create_inventory_agent

# Load environment variables from .env file
load_dotenv()

async def test_agent(prompt: str):
    """Test the agent with a specific prompt."""
    print(f"\n{'='*70}")
    print(f"TEST: {prompt}")
    print(f"{'='*70}\n")
    
    agent = create_inventory_agent()
    session_service = InMemorySessionService()
    app_name = "inventory_app"
    
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service
    )
    
    session_id = str(uuid.uuid4())
    user_id = "user-1"
    
    try:
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        part = types.Part(text=prompt)
        content = types.Content(role="user", parts=[part])
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if hasattr(event, 'content') and event.content:
                parts = event.content.parts
                
                for part in parts:
                    if hasattr(part, 'text') and part.text:
                        print(f"🤖 Agent: {part.text}\n")
                    
                    if hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        if hasattr(fc, 'args') and fc.args:
                            args_str = ", ".join(f"{k}={repr(v)}" for k, v in fc.args.items())
                        else:
                            args_str = ""
                        name = fc.name if hasattr(fc, 'name') else str(fc)
                        print(f"🔧 Tool: {name}({args_str})")
                    
                    if hasattr(part, 'function_response') and part.function_response:
                        fr = part.function_response 
                        if hasattr(fr, 'response'):
                            result = fr.response
                        elif hasattr(fr, '__dict__'):
                            result = fr.__dict__
                        else:
                            result = str(fr)
                        print(f"✓ Result: {result}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Run multiple test scenarios."""
    
    # Test 1: On-topic - Check stock
    await test_agent("What's the current stock of Smartphone?")
    
    # Test 2: On-topic - Inventory question
    await test_agent("How many different products do we have in inventory?")
    
    # Test 3: Off-topic - Weather
    await test_agent("What's the weather like today?")
    
    # Test 4: Off-topic - General chat
    await test_agent("Tell me a joke")
    
    # Test 5: On-topic - Restock request
    await test_agent("Check laptop stock and restock if needed")
    
    print(f"\n{'='*70}")
    print("ALL TESTS COMPLETE")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(main())
