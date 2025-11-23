"""
Conversation persistence for MySQL.
Stores user questions, agent reasoning, and responses.
"""

import os
from datetime import datetime
from typing import Optional, List, Dict
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

class ConversationLogger:
    """Logs conversations to MySQL for persistence and analysis."""
    
    def __init__(self):
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', 'inventory_db'),
            'port': int(os.getenv('MYSQL_PORT', 3306))
        }
        self.use_mysql = os.getenv('USE_MYSQL', 'false').lower() == 'true'
    
    def _get_connection(self):
        """Create database connection."""
        if not self.use_mysql:
            return None
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            print(f"Warning: Could not connect to MySQL for conversation logging: {e}")
            return None
    
    def init_tables(self):
        """Initialize conversation tables if they don't exist."""
        if not self.use_mysql:
            return
        
        conn = self._get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Create conversations table
            create_table = """
            CREATE TABLE IF NOT EXISTS conversations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id VARCHAR(255),
                user_message TEXT,
                agent_reasoning TEXT,
                agent_response TEXT,
                tools_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_session (session_id),
                INDEX idx_created (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            cursor.execute(create_table)
            conn.commit()
            print("✓ Conversation logging tables ready")
            
        except Error as e:
            print(f"Error creating conversation tables: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def log_conversation(
        self,
        session_id: str,
        user_message: str,
        agent_reasoning: Optional[str] = None,
        agent_response: Optional[str] = None,
        tools_used: Optional[List[str]] = None
    ):
        """Log a conversation turn to MySQL."""
        if not self.use_mysql:
            return
        
        conn = self._get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            tools_str = ", ".join(tools_used) if tools_used else None
            
            insert_query = """
            INSERT INTO conversations 
            (session_id, user_message, agent_reasoning, agent_response, tools_used)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                session_id,
                user_message,
                agent_reasoning,
                agent_response,
                tools_str
            ))
            conn.commit()
            
        except Error as e:
            print(f"Error logging conversation: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def get_conversation_history(
        self,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """Retrieve conversation history."""
        if not self.use_mysql:
            return []
        
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            if session_id:
                query = """
                SELECT * FROM conversations 
                WHERE session_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s
                """
                cursor.execute(query, (session_id, limit))
            else:
                query = """
                SELECT * FROM conversations 
                ORDER BY created_at DESC 
                LIMIT %s
                """
                cursor.execute(query, (limit,))
            
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error retrieving conversation history: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# Global conversation logger
conversation_logger = ConversationLogger()
