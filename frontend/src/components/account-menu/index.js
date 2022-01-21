import cn from 'classnames'
import styles from './styles.module.css'
import { useContext } from 'react'
import { Button, LinkComponent } from '../index.js'
import { AuthContext } from '../../contexts'

const AccountMenu = ({ onSignOut }) => {
  const authContext = useContext(AuthContext)
  if (!authContext) {
    return <div className={styles.menu}>
      <LinkComponent
        className={styles.menuLink}
        href='/signin'
        title='Войти'
      />
      <LinkComponent
        href='/signup'
        title='Создать аккаунт'
        className={styles.menuButton}
      />
    </div>
  }
  return <div className={styles.menu}>
    <LinkComponent
      className={styles.menuLink}
      href='/change-password'
      title='Изменить пароль'
    />
    <a
      className={styles.menuLink}
      onClick={onSignOut}
    >
      Выход
    </a>
  </div>
}


export default AccountMenu