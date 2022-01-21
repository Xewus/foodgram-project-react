import styles from './style.module.css'
import { Nav, AccountMenu } from '../index.js'
import Container from '../container'

const Header = ({ loggedIn, onSignOut, orders }) => {
  return <header
    className={styles.header}
  >
    <Container>
      <div className={styles.headerContent}>
        <Nav loggedIn={loggedIn} orders={orders} />
        <AccountMenu onSignOut={onSignOut} />
      </div>
    </Container>
  </header>
}

export default Header
